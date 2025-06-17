import azure.functions as func
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    HTTP-triggered function to test the activity function logic independently
    """
    try:
        logger.info("🧪 TEST ACTIVITY FUNCTION: HTTP trigger fired!")
        
        # Test the activity function logic
        test_input = {
            "chunk_id": 0,
            "start": "2025-06-16T15:00:00.000000Z",
            "end": "2025-06-16T15:10:00.000000Z",
            "time": "2025-06-16T15:00:00.000000Z",
            "total_chunks": 5
        }
        
        # Import and call the activity function
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'process_chunk_activity'))
        
        from process_chunk_activity.app import main as activity_main
        
        logger.info("🔧 TEST ACTIVITY FUNCTION: Calling process_chunk_activity...")
        result = activity_main(test_input)
        
        logger.info(f"✅ TEST ACTIVITY FUNCTION: Activity result: {result}")
        
        response_data = {
            "success": True,
            "message": "Activity function test completed successfully",
            "input": test_input,
            "result": result
        }
        
        return func.HttpResponse(
            json.dumps(response_data, indent=2),
            status_code=200,
            mimetype="application/json"
        )
        
    except Exception as e:
        error_message = f"❌ TEST ACTIVITY FUNCTION ERROR: {str(e)}"
        logger.error(error_message, exc_info=True)
        
        error_response = {
            "success": False,
            "error": str(e),
            "message": "Activity function test failed"
        }
        
        return func.HttpResponse(
            json.dumps(error_response, indent=2),
            status_code=500,
            mimetype="application/json"
        )
