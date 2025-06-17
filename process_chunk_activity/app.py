import logging
import time
import random

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main(input):
    """
    Activity function that processes a single chunk of data (async)
    """
    try:
        logger.info("⚡ ACTIVITY FUNCTION: Starting chunk processing!")
        # Extract input parameters
        chunk_id = input["chunk_id"]
        start = input["start"]
        end = input["end"]
        bucket_time = input["time"]
        total_chunks = input.get("total_chunks", "unknown")

        logger.info(f"📦 ACTIVITY FUNCTION: Processing chunk {chunk_id} of {total_chunks}")
        logger.info(f"   - Start time: {start}")
        logger.info(f"   - End time: {end}")
        logger.info(f"   - Bucket time: {bucket_time}")        # Simulate some realistic processing work
        processing_time = random.uniform(0.5, 2.0)  # Random processing time between 0.5-2 seconds
        logger.info(f"🔄 ACTIVITY FUNCTION: Simulating {processing_time:.2f}s of processing work for chunk {chunk_id}")
        
        time.sleep(processing_time)  # Use regular sleep for v1 programming model
        # Simulate processing different types of data
        data_types = ["sensor_data", "log_entries", "user_events", "system_metrics"]
        processed_data_type = random.choice(data_types)
        records_processed = random.randint(30, 50)
        
        logger.info(f"📊 ACTIVITY FUNCTION: Processed {records_processed} {processed_data_type} records")
          # Create detailed result - ensure all values are JSON serializable
        result = {
            "chunk_id": int(chunk_id),
            "status": "success",
            "records_processed": int(records_processed),
            "data_type": str(processed_data_type),
            "processing_time_seconds": float(round(processing_time, 2)),
            "start_time": str(start),
            "end_time": str(end)
        }
        
        success_message = f"✅ ACTIVITY FUNCTION: Chunk {chunk_id} completed successfully! Processed {records_processed} {processed_data_type} records in {processing_time:.2f}s"
        logger.info(success_message)
        
        return result
        
    except Exception as e:
        error_message = f"❌ ACTIVITY FUNCTION ERROR in chunk {input.get('chunk_id', 'unknown')}: {str(e)}"
        logger.error(error_message, exc_info=True)
          # Return error result instead of raising to avoid breaking the orchestration
        return {
            "chunk_id": int(input.get("chunk_id", 0)),
            "status": "error",
            "error": str(e),
            "records_processed": 0
        }
