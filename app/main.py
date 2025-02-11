import hydra
from omegaconf import DictConfig
import mlflow

@hydra.main(config_path="app/config", config_name="config")
def main(cfg: DictConfig):
    mlflow.set_tracking_uri(cfg.mlflow.tracking_uri)
    mlflow.set_experiment(cfg.mlflow.experiment_name)
    
    # Add training pipeline here
    pass

if __name__ == "__main__":
    main()
