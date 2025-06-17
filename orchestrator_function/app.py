import azure.durable_functions as df
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def orchestrator_function(context: df.DurableOrchestrationContext):
    """
    Orchestrator function that coordinates the processing of chunks using call_activity (generator pattern)
    """
    logger.info("🎼 ORCHESTRATOR FUNCTION: Starting orchestration!")
    logger.info("✅ ORCHESTRATOR FUNCTION: Successfully imported azure.durable_functions")
    
    # Get input data
    try:
        input_data = context.get_input()
        logger.info(f"📥 ORCHESTRATOR FUNCTION: Input data: {input_data}")
    except Exception as e:
        logger.error(f"⚠️ ORCHESTRATOR FUNCTION: Error getting input: {str(e)}")
        input_data = None
        
    # Set defaults if no input data
    if not input_data:
        logger.info("📥 ORCHESTRATOR FUNCTION: Using default test data")
        input_data = {
            "start": "2025-06-16T14:53:00.078585Z",
            "end": "2025-06-16T15:03:00.078585Z", 
            "total_chunks": 3,  # Start small for testing
            "time": "2025-06-16T14:53:00.078585Z"
        }
    
    # Extract parameters
    start = input_data.get("start", "unknown")
    end = input_data.get("end", "unknown")
    total_chunks = input_data.get("total_chunks", 3)
    time = input_data.get("time", "unknown")
    
    logger.info(f"📝 ORCHESTRATOR FUNCTION: Processing parameters:")
    logger.info(f"   - Start: {start}")
    logger.info(f"   - End: {end}")
    logger.info(f"   - Total chunks: {total_chunks}")
    logger.info(f"   - Time: {time}")
    
    # Validate and limit chunks
    if not isinstance(total_chunks, int) or total_chunks <= 0:
        total_chunks = 3
        logger.warning(f"⚠️ ORCHESTRATOR FUNCTION: Using default total_chunks = {total_chunks}")
    
    if total_chunks > 5:  # Keep it small for testing
        total_chunks = 5
        logger.info(f"🔧 ORCHESTRATOR FUNCTION: Limited total_chunks to {total_chunks} for testing")
    
    logger.info(f"🚀 ORCHESTRATOR FUNCTION: Processing {total_chunks} chunks using fan-out/fan-in parallel pattern")
    
    # FAN-OUT: Create all activity tasks in parallel (don't yield yet!)
    tasks = []
    
    for chunk_id in range(int(total_chunks)):
        logger.info(f"📤 ORCHESTRATOR FUNCTION: Queuing ProcessChunkActivity for chunk {chunk_id}")
        
        # Prepare chunk data - ensure all values are JSON serializable
        chunk_data = {
            "chunk_id": int(chunk_id),
            "start": str(start),
            "end": str(end),
            "total_chunks": int(total_chunks),
            "time": str(time)
        }
        
        # ⭐ Create the task but DON'T yield yet - this allows parallel execution
        task = context.call_activity("ProcessChunkActivity", chunk_data)
        tasks.append(task)
    
    logger.info(f"🔀 ORCHESTRATOR FUNCTION: Fan-out complete! {len(tasks)} tasks queued for parallel execution")
    
    try:
        # FAN-IN: Wait for ALL tasks to complete in parallel
        logger.info("⏳ ORCHESTRATOR FUNCTION: Waiting for all tasks to complete...")
        results = yield context.task_all(tasks)
        logger.info(f"✅ ORCHESTRATOR FUNCTION: All {len(results)} chunks completed in parallel!")
        
    except Exception as e:
        logger.error(f"❌ ORCHESTRATOR FUNCTION: Error in parallel execution: {str(e)}")
        # Return partial results if some tasks failed
        results = [{"error": str(e), "status": "failed"}]
    
    logger.info(f"✅ ORCHESTRATOR FUNCTION: All {total_chunks} chunks processed!")
    logger.info(f"🎉 ORCHESTRATOR FUNCTION: Orchestration completed with {len(results)} results")
    
    # Return the results - ensure all data is JSON serializable
    final_result = {
        "status": "completed",
        "total_chunks": int(total_chunks),
        "results": results
    }
    
    logger.info(f"📤 ORCHESTRATOR FUNCTION: Returning result: {final_result}")
    return final_result

# Register the orchestrator function
main = df.Orchestrator.create(orchestrator_function)
