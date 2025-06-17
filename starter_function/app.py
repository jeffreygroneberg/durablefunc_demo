import azure.durable_functions as df
import azure.functions as func
import os
import requests
import json
import logging
import datetime
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main(timer, starter):
    """
    Timer-triggered starter function that initiates the durable orchestration
    """
    try:
        logger.info("🚀 STARTER FUNCTION: Timer trigger fired!")
        logger.info(f"🕒 Timer trigger time: {timer}")
        
        # Log successful import
        logger.info("✅ STARTER FUNCTION: Successfully imported azure.durable_functions")
        
        # Create durable orchestration client
        client = df.DurableOrchestrationClient(starter)
        logger.info("✅ STARTER FUNCTION: DurableOrchestrationClient created successfully")
        
        # Define time parameters
        timedelta = 10  # (in minutes)
        ago_10min = datetime.datetime.utcnow() - datetime.timedelta(minutes=10)
        ago_10min_iso = ago_10min.isoformat() + "Z"
        start = ago_10min_iso
        end = (ago_10min + datetime.timedelta(minutes=timedelta)).isoformat() + "Z"        # Define processing parameters
        chunk_size = 40  # Define chunk size
        total_rows = 200  # Reduced for parallel testing
        total_chunks = int(total_rows / chunk_size)

        logger.info(f"📊 STARTER FUNCTION: Processing parameters:")
        logger.info(f"   - Start time: {start}")
        logger.info(f"   - End time: {end}")
        logger.info(f"   - Total chunks: {total_chunks}")
        logger.info(f"   - Chunk size: {chunk_size}")
        logger.info(f"   - Total rows: {total_rows}")

        # Start the orchestration
        input_data = {
            "start": start,
            "end": end,
            "total_chunks": total_chunks,
            "time": ago_10min_iso
        }
        
        logger.info("🎯 STARTER FUNCTION: Starting orchestration...")
        instance_id = await client.start_new("orchestrator_function", None, input_data)
        
        success_message = f"✅ STARTER FUNCTION: Successfully started orchestration with ID = '{instance_id}'"
        logger.info(success_message)
        
        # For now, just log the instance ID - status checking can be added later
        logger.info(f"🔗 STARTER FUNCTION: Instance ID for tracking: {instance_id}")
        
        # Timer triggers don't need return values - just log the success
        logger.info("🎯 STARTER FUNCTION: Timer trigger completed successfully")
        
    except Exception as e:
        error_message = f"❌ STARTER FUNCTION ERROR: {str(e)}"
        logger.error(error_message, exc_info=True)
        raise e