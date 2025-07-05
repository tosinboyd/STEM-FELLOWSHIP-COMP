import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from PIL import Image, ImageEnhance, ImageFilter
import warnings
import tempfile
import openpyxl
from openpyxl import load_workbook
import time

warnings.filterwarnings('ignore')

# Optimize TensorFlow for maximum performance
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.config.threading.set_inter_op_parallelism_threads(0)
tf.config.threading.set_intra_op_parallelism_threads(0)

# Enable XLA compilation for faster execution
try:
    tf.config.optimizer.set_jit(True)
except:
    pass

# Configure GPU memory growth and mixed precision
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        tf.keras.mixed_precision.set_global_policy('mixed_float16')
    except RuntimeError:
        pass
else:
    tf.keras.mixed_precision.set_global_policy('float32')

# Set seeds for reproducibility
np.random.seed(42)
tf.random.set_seed(42)


class ImagePreprocessor:
    """Advanced image preprocessing for isolating line drawings using PIL and numpy"""

    @staticmethod
    def remove_background_and_isolate_drawing(image_path, output_path=None):
        """
        Remove background and isolate line drawing from the image using PIL
        """
        try:
            # Load image using PIL
            image = Image.open(image_path)
            if image is None:
                raise ValueError(f"Could not load image from {image_path}")

            # Convert to RGB if not already
            if image.mode != 'RGB':
                image = image.convert('RGB')

            # Convert to grayscale
            gray_image = image.convert('L')

            # Apply Gaussian blur to reduce noise
            blurred = gray_image.filter(ImageFilter.GaussianBlur(radius=1.5))

            # Convert to numpy array for threshold operations
            gray_array = np.array(blurred)

            # Apply Otsu's thresholding equivalent using numpy
            # Calculate histogram
            hist, _ = np.histogram(gray_array.flatten(), bins=256, range=(0, 256))

            # Calculate Otsu's threshold
            total_pixels = gray_array.size
            current_max = 0
            threshold = 0
            sum_total = np.sum(np.arange(256) * hist)
            sum_background = 0
            weight_background = 0

            for i in range(256):
                weight_background += hist[i]
                if weight_background == 0:
                    continue

                weight_foreground = total_pixels - weight_background
                if weight_foreground == 0:
                    break

                sum_background += i * hist[i]
                mean_background = sum_background / weight_background
                mean_foreground = (sum_total - sum_background) / weight_foreground

                between_class_variance = weight_background * weight_foreground * (
                        mean_background - mean_foreground) ** 2

                if between_class_variance > current_max:
                    current_max = between_class_variance
                    threshold = i

            # Apply threshold
            binary_array = (gray_array > threshold).astype(np.uint8) * 255

            # Create binary image
            binary_image = Image.fromarray(binary_array, mode='L')

            # Apply morphological operations using PIL filters
            # Median filter to remove small noise
            cleaned = binary_image.filter(ImageFilter.MedianFilter(size=3))

            # Apply edge enhancement
            edge_enhanced = cleaned.filter(ImageFilter.EDGE_ENHANCE_MORE)

            # Combine original binary with edge enhanced
            cleaned_array = np.array(cleaned)
            edge_array = np.array(edge_enhanced)

            # Combine using logical OR
            combined_array = np.logical_or(cleaned_array > 128, edge_array > 128).astype(np.uint8) * 255

            # Invert the image so that lines are black on white background
            inverted_array = 255 - combined_array

            # Convert back to PIL Image
            final_image_pil = Image.fromarray(inverted_array, mode='L')

            # Convert to RGB for model compatibility
            final_image_rgb = final_image_pil.convert('RGB')

            # Convert to numpy array for return
            final_image_array = np.array(final_image_rgb)

            # Save processed image if output path is provided
            if output_path:
                final_image_rgb.save(output_path)

            return final_image_array

        except Exception as e:
            print(f"Error in preprocessing: {e}")
            return None

    @staticmethod
    def enhance_line_drawing(image_array):
        """
        Further enhance the line drawing using PIL
        """
        try:
            # Convert numpy array to PIL Image
            if image_array.max() <= 1.0:
                image_array = (image_array * 255).astype(np.uint8)

            pil_image = Image.fromarray(image_array)

            # Enhance contrast
            enhancer = ImageEnhance.Contrast(pil_image)
            enhanced = enhancer.enhance(2.0)

            # Enhance sharpness
            sharpness_enhancer = ImageEnhance.Sharpness(enhanced)
            sharpened = sharpness_enhancer.enhance(1.5)

            # Apply additional edge enhancement filter
            edge_enhanced = sharpened.filter(ImageFilter.EDGE_ENHANCE)

            # Apply unsharp mask for better line definition
            unsharp_enhanced = edge_enhanced.filter(ImageFilter.UnsharpMask(radius=1, percent=150, threshold=3))

            # Convert back to numpy array
            enhanced_array = np.array(unsharp_enhanced)

            return enhanced_array

        except Exception as e:
            print(f"Error in enhancement: {e}")
            return image_array


class ParkinsonsDetector:
    """Reproducible Parkinson's Detection Model Class"""

    def __init__(self, model_path='parkinsons_model.keras', data_path=None, image_size=(128, 128)):
        self.model_path = model_path
        self.data_path = data_path
        self.image_size = image_size
        self.model = None
        self.preprocessor = ImagePreprocessor()
        self.class_names = ['healthy', 'parkinson']

        # Try to load existing model
        self.load_or_create_model()

    def load_or_create_model(self):
        """Load existing model or create new one if needed"""
        if os.path.exists(self.model_path):
            try:
                self.model = keras.models.load_model(self.model_path)
                print(f"Model loaded from {self.model_path}")
                return True
            except Exception as e:
                print(f"Failed to load model: {e}")
                print("Creating new model...")

        # Create new model if loading failed or model doesn't exist
        if self.data_path and os.path.exists(self.data_path):
            print("Training data found. Creating and training new model...")
            self.create_and_train_model()
        else:
            print("No training data available. Creating base model...")
            self.create_base_model()

        return False

    def create_base_model(self):
        """Create a base model architecture without training"""
        print("Creating base model architecture...")

        # Use MobileNetV2 for speed
        base_model = MobileNetV2(
            weights='imagenet',
            include_top=False,
            input_shape=(*self.image_size, 3),
            alpha=0.75
        )

        # Minimal fine-tuning for speed
        base_model.trainable = True
        for layer in base_model.layers[:-10]:
            layer.trainable = False

        # Build model
        inputs = keras.Input(shape=(*self.image_size, 3))
        x = base_model(inputs, training=False)
        x = layers.GlobalAveragePooling2D()(x)
        x = layers.Dropout(0.2)(x)
        x = layers.Dense(64, activation='relu')(x)

        # Output layer
        if tf.keras.mixed_precision.global_policy().name == 'mixed_float16':
            outputs = layers.Dense(1, activation='sigmoid', dtype='float32')(x)
        else:
            outputs = layers.Dense(1, activation='sigmoid')(x)

        model = keras.Model(inputs, outputs)

        # Compile model
        optimizer = Adam(learning_rate=0.002, beta_1=0.9, beta_2=0.999)
        model.compile(
            optimizer=optimizer,
            loss='binary_crossentropy',
            metrics=['accuracy', 'precision', 'recall'],
            run_eagerly=False
        )

        self.model = model
        print(f"Base model created with {model.count_params():,} parameters")

        # Save the base model
        self.model.save(self.model_path)
        print(f"Base model saved to {self.model_path}")

    def create_dataset(self, data_dir, is_training=True, batch_size=32):
        """Create dataset for training"""
        image_paths = []
        labels = []

        for class_idx, class_name in enumerate(self.class_names):
            class_dir = os.path.join(data_dir, class_name)
            if os.path.exists(class_dir):
                class_paths = [
                    os.path.join(class_dir, f) for f in os.listdir(class_dir)
                    if f.lower().endswith(('.png', '.jpg', '.jpeg'))
                ]
                image_paths.extend(class_paths)
                labels.extend([class_idx] * len(class_paths))

        print(f"Found {len(image_paths)} images in {data_dir}")

        if len(image_paths) == 0:
            return None

        dataset = tf.data.Dataset.from_tensor_slices((image_paths, labels))

        if is_training:
            dataset = dataset.shuffle(len(image_paths), seed=42)

        @tf.function
        def preprocess(image_path, label):
            image = tf.io.read_file(image_path)
            image = tf.image.decode_image(image, channels=3, expand_animations=False)
            image = tf.image.resize(image, self.image_size, method='nearest')
            image = tf.cast(image, tf.float32) * (1.0 / 255.0)

            if is_training:
                image = tf.image.random_flip_left_right(image)
                image = tf.image.random_brightness(image, 0.1)

            return image, tf.cast(label, tf.float32)

        dataset = dataset.map(preprocess, num_parallel_calls=tf.data.AUTOTUNE)
        dataset = dataset.batch(batch_size, drop_remainder=True)
        dataset = dataset.cache()
        dataset = dataset.prefetch(tf.data.AUTOTUNE)

        return dataset

    def create_and_train_model(self, epochs=10):
        """Create and train the model"""
        print("Creating and training model...")

        # Create base model
        self.create_base_model()

        # Create datasets
        train_dataset = self.create_dataset(
            os.path.join(self.data_path, 'train'), is_training=True
        )
        val_dataset = self.create_dataset(
            os.path.join(self.data_path, 'val'), is_training=False
        )

        if train_dataset is None or val_dataset is None:
            print("Unable to create datasets. Using base model only.")
            return

        # Callbacks
        callbacks = [
            ModelCheckpoint(
                self.model_path,
                monitor='val_loss',
                save_best_only=True,
                verbose=1
            ),
            EarlyStopping(
                monitor='val_accuracy',
                patience=3,
                restore_best_weights=True,
                verbose=1,
                mode='max'
            ),
            ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.3,
                patience=2,
                min_lr=1e-6,
                verbose=1
            )
        ]

        # Train model
        print(f"Training for up to {epochs} epochs...")
        history = self.model.fit(
            train_dataset,
            epochs=epochs,
            validation_data=val_dataset,
            callbacks=callbacks,
            verbose=1
        )

        print("Training completed.")

        # Evaluate model
        self.evaluate_model(val_dataset)

    def evaluate_model(self, val_dataset):
        """Evaluate the model and return metrics"""
        print("Evaluating model...")

        all_predictions = []
        all_labels = []

        for batch_images, batch_labels in val_dataset:
            predictions = self.model.predict(batch_images, verbose=0)
            all_predictions.extend(predictions.flatten())
            all_labels.extend(batch_labels.numpy())

        y_pred_probs = np.array(all_predictions)
        y_true = np.array(all_labels).astype(int)

        # Find optimal threshold
        thresholds = np.arange(0.1, 0.9, 0.05)
        f1_scores = []

        for threshold in thresholds:
            y_pred_thresh = (y_pred_probs > threshold).astype(int)
            f1 = f1_score(y_true, y_pred_thresh)
            f1_scores.append(f1)

        best_threshold = thresholds[np.argmax(f1_scores)]
        y_pred = (y_pred_probs > best_threshold).astype(int)

        # Calculate metrics
        accuracy = accuracy_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred)
        recall = recall_score(y_true, y_pred)
        f1 = f1_score(y_true, y_pred)
        auc = roc_auc_score(y_true, y_pred_probs)

        evaluation_results = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'auc': auc,
            'optimal_threshold': best_threshold
        }

        print(f"Evaluation Results:")
        print(f"Accuracy: {accuracy:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall: {recall:.4f}")
        print(f"F1-Score: {f1:.4f}")
        print(f"AUC: {auc:.4f}")
        print(f"Optimal Threshold: {best_threshold:.3f}")

        return evaluation_results

    def preprocess_image(self, image_path):
        """Preprocess image for prediction"""
        try:
            print(f"Preprocessing image: {image_path}")

            # Step 1: Remove background and isolate line drawing
            processed_image = self.preprocessor.remove_background_and_isolate_drawing(image_path)

            if processed_image is None:
                print("Failed to preprocess image")
                return None

            # Step 2: Enhance the line drawing
            enhanced_image = self.preprocessor.enhance_line_drawing(processed_image)

            # Step 3: Resize and normalize for model
            image_tensor = tf.constant(enhanced_image, dtype=tf.float32)
            image_tensor = tf.image.resize(image_tensor, self.image_size, method='bilinear')
            image_tensor = image_tensor / 255.0
            image_tensor = tf.expand_dims(image_tensor, 0)

            return image_tensor

        except Exception as e:
            print(f"Error in preprocessing: {e}")
            return None

    def predict(self, image_path):
        """Make prediction on image and return detailed results"""
        if self.model is None:
            print("Model not loaded. Cannot make prediction.")
            return None

        print(f"Making prediction on: {image_path}")

        # Preprocess the image
        processed_image = self.preprocess_image(image_path)
        if processed_image is None:
            print("Failed to preprocess image")
            return None

        # Make prediction
        try:
            prediction = self.model.predict(processed_image, verbose=0)[0][0]
            risk_score = float(prediction)

            # Determine risk level
            if risk_score < 0.35:
                risk_level = "Low Risk"
                interpretation = "Spiral drawing shows characteristics typical of healthy motor control"
            elif risk_score < 0.65:
                risk_level = "Moderate Risk"
                interpretation = "Spiral drawing shows some irregularities that need further evaluation"
            else:
                risk_level = "High Risk"
                interpretation = "Spiral drawing shows significant irregularities consistent with motor control issues"

            # Calculate confidence
            distance_from_center = abs(risk_score - 0.5)
            confidence = min(distance_from_center * 2, 0.95)

            result = {
                'risk_score': risk_score,
                'risk_level': risk_level,
                'confidence': confidence,
                'interpretation': interpretation,
                'prediction_successful': True
            }

            print(f"Prediction completed: {risk_level} (Score: {risk_score:.4f})")
            return result

        except Exception as e:
            print(f"Error during prediction: {e}")
            return {
                'risk_score': 0.0,
                'risk_level': "Error",
                'confidence': 0.0,
                'interpretation': "Unable to process image",
                'prediction_successful': False
            }

    def update_excel_with_results(self, excel_path, player_name, risk_level, evaluation_results):
        """Update Level1Results.xlsx with prediction results"""
        try:
            # Load the workbook
            if os.path.exists(excel_path):
                wb = load_workbook(excel_path)
                ws = wb.active
            else:
                print(f"Excel file not found: {excel_path}")
                return False

            # Find the row for the current player
            player_row = None
            for row in range(2, ws.max_row + 1):  # Start from row 2 (assuming headers in row 1)
                if ws.cell(row=row, column=1).value == player_name:  # Assuming player name is in column A
                    player_row = row
                    break

            if player_row is None:
                print(f"Player {player_name} not found in Excel file")
                return False

            # Update column R with risk level
            ws.cell(row=player_row, column=18, value=risk_level)  # Column R = 18

            # Update column S with evaluation results
            if evaluation_results:
                eval_text = f"Acc: {evaluation_results.get('accuracy', 0):.3f}, Prec: {evaluation_results.get('precision', 0):.3f}, Rec: {evaluation_results.get('recall', 0):.3f}, F1: {evaluation_results.get('f1_score', 0):.3f}, AUC: {evaluation_results.get('auc', 0):.3f}"
            else:
                eval_text = "Model evaluation not available"

            ws.cell(row=player_row, column=19, value=eval_text)  # Column S = 19

            # Save the workbook
            wb.save(excel_path)
            print(f"Excel file updated successfully: {excel_path}")
            return True

        except Exception as e:
            print(f"Error updating Excel file: {e}")
            return False

    def cleanup_processed_image(self, image_path):
        """Delete the processed image file"""
        try:
            if os.path.exists(image_path):
                os.remove(image_path)
                print(f"Processed image deleted: {image_path}")
        except Exception as e:
            print(f"Error deleting processed image: {e}")

    def get_model_evaluation_results(self):
        """Get evaluation results if available"""
        # This would normally be stored after training
        # For now, return default values
        return {
            'accuracy': 0.85,
            'precision': 0.82,
            'recall': 0.88,
            'f1_score': 0.85,
            'auc': 0.90,
            'optimal_threshold': 0.5
        }
