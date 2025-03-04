"""
Yellow Taxi Data Validation Checkpoint Runner
-------------------------------------------
This script runs the pre-configured Great Expectations checkpoint for yellow taxi data validation.

Prerequisites:
- Great Expectations context must be initialized (gx directory must exist)
- Checkpoint 'yellowtaxi_data_validation_checkpoint' must be configured
- PostgreSQL database must be accessible
- Conda environment 'gxcore-env' must be created (see README.md for setup instructions)

Usage:
    # Using conda run (recommended):
    conda run -n gxcore-env python yellowtaxi_expectations_runcheckpoint.py

    # OR activate environment first:
    conda activate gxcore-env
    python yellowtaxi_expectations_runcheckpoint.py

Note:
    For environment setup and detailed instructions, please refer to README.md
"""

import sys
import logging
from pathlib import Path
import great_expectations as gx

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def validate_prerequisites():
    """Verify that all required components are in place."""
    gx_dir = Path("./gx")
    if not gx_dir.exists():
        raise RuntimeError("GX directory not found. Please run the setup notebook first.")
    logger.info("GX directory found, proceeding with validation")

def run_checkpoint():
    """Run the validation checkpoint and return results."""
    try:
        # Get existing context
        context = gx.get_context(mode="file")
        logger.info("Successfully loaded GX context")

        # Get the Checkpoint
        checkpoint_name = "yellowtaxi_data_validation_checkpoint"
        checkpoint = context.checkpoints.get(checkpoint_name)
        if not checkpoint:
            raise ValueError(f"Checkpoint '{checkpoint_name}' not found")
        logger.info(f"Found checkpoint: {checkpoint_name}")

        # Run the Checkpoint
        logger.info("Starting validation...")
        validation_results = checkpoint.run()
        logger.info("Validation completed")

        return validation_results

    except Exception as e:
        logger.error(f"Error during validation: {str(e)}")
        raise

def main():
    """Main execution function."""
    try:
        validate_prerequisites()
        results = run_checkpoint()
        
        # Log validation success/failure
        if results.success:
            logger.info("Validation successful!")
        else:
            logger.warning("Validation failed - check Data Docs for details")
            
        logger.info("Results available in Data Docs at: ./gx/uncommitted/data_docs/local_site/index.html")
        return 0 if results.success else 1

    except Exception as e:
        logger.error(f"Script execution failed: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())