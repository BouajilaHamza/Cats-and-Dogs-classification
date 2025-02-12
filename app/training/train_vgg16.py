import os
import tensorflow as tf
from tensorflow.keras import layers, Sequential
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from comet_ml import Experiment
from app.core.config import settings  # Assumes new config parameters are added

def get_data_generators(train_dir, val_dir, target_size=(128,128), batch_size=128):
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=0.2,
        width_shift_range=0.2,
        height_shift_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True
    )
    val_datagen = ImageDataGenerator(rescale=1./255)
    train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=target_size,
        batch_size=batch_size,
        class_mode='binary'
    )
    validation_generator = val_datagen.flow_from_directory(
        val_dir,
        target_size=target_size,
        batch_size=batch_size,
        class_mode='binary'
    )
    return train_generator, validation_generator

def build_model(input_shape=(128,128,3)):
    conv_base = VGG16(input_shape=input_shape, include_top=False, weights='imagenet')
    for layer in conv_base.layers:
        layer.trainable = False
    model = Sequential([
        conv_base,
        layers.Flatten(),
        layers.Dense(256, activation='relu'),
        layers.Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

def train_model(train_dir, val_dir, epochs):
    # Initialize Comet ML experiment
    experiment = Experiment(
        api_key=settings.COMET_API_KEY,
        project_name=settings.PROJECT_NAME,
        workspace=settings.COMET_WORKSPACE
    )
    experiment.set_name("vgg16_training_pipeline")
    
    train_gen, val_gen = get_data_generators(train_dir, val_dir, batch_size=settings.BATCH_SIZE)
    model = build_model()
    
    # Define callback to log metrics to Comet ML
    comet_callback = tf.keras.callbacks.LambdaCallback(
        on_epoch_end=lambda epoch, logs: experiment.log_metrics(logs, step=epoch)
    )
    
    history = model.fit(
        train_gen,
        steps_per_epoch=train_gen.samples // train_gen.batch_size,
        epochs=epochs,
        validation_data=val_gen,
        validation_steps=val_gen.samples // val_gen.batch_size,
        callbacks=[comet_callback]
    )
    experiment.log_metric("final_train_loss", history.history['loss'][-1])
    experiment.log_metric("final_val_loss", history.history['val_loss'][-1])
    
    # Save model artifact
    model_dir = os.path.join(os.getcwd(), "app", "models")
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "vgg16_model.h5")
    model.save(model_path)
    experiment.log_asset(file_data=model_path, file_name="vgg16_model.h5")
    
    experiment.end()

# if __name__ == '__main__':
#     # Fetch directories and hyperparameters from config
#     train_directory = settings.TRAIN_DIR  # e.g. "app/data/training_set"
#     val_directory = settings.VAL_DIR      # e.g. "app/data/validation_set"
#     train_model(train_directory, val_directory, epochs=settings.EPOCHS)
