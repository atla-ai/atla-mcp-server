from mcp.server.fastmcp import FastMCP
import os
from atla import AsyncAtla, Atla
from typing import Optional, List, Dict, Any
import asyncio
import uvicorn 
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the MCP server
mcp = FastMCP("AtlaEvaluator")

# Initialize Atla client
# Note: API key will be taken from environment variable ATLA_API_KEY
atla_client = Atla(api_key=os.environ.get("ATLA_API_KEY"))
atla_async_client = AsyncAtla(api_key=os.environ.get("ATLA_API_KEY"))

@mcp.tool()
async def evaluate_response(
    model_input: str,
    model_output: str,
    evaluation_criteria: str,
    expected_model_output: Optional[str] = None,
    model_context: Optional[str] = None,
    model_id: str = "atla-selene"
) -> Dict[str, str]:
    """
    Evaluate an LLM response using Atla's evaluation model.

    This function takes evaluation parameters and sends them to the Atla API for evaluation.
    It returns a dictionary containing the evaluation score and critique.

    Args:
        model_input (str): The prompt or question given to the model to generate the response.
        model_output (str): The response generated by the model that needs to be evaluated.
        evaluation_criteria (str): The specific criteria or instructions for evaluating the model's output.
        expected_model_output (Optional[str]): A reference or ideal answer to compare against the model's output. Defaults to None.
        model_context (Optional[str]): Additional context or information provided to the model during generation. Defaults to None.
        model_id (str): The identifier of the Atla evaluation model to use. Defaults to "atla-selene".

    Returns:
        Dict[str, str]: A dictionary containing two keys:
            - "score": The numerical evaluation score assigned by the Atla model.
            - "critique": A textual explanation or critique of the evaluation.
    """
    result = await atla_async_client.evaluation.create(
        model_id=model_id,
        model_input=model_input,
        model_output=model_output,
        evaluation_criteria=evaluation_criteria,
        expected_model_output=expected_model_output,
        few_shot_examples=[],
        model_context=model_context,
    )
    
    return {
        "score": result.result.evaluation.score,
        "critique": result.result.evaluation.critique,
    }

@mcp.tool()
async def batch_evaluate_responses(evaluations: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """
    Perform batch evaluation of multiple LLM responses using Atla's evaluation model.

    This function takes a list of evaluation requests and processes them concurrently using asyncio.
    It returns a list of evaluation responses.

    Args:
        evaluations (List[Dict[str, Any]]): A list of dictionaries, each containing the parameters for a single evaluation:
            - model_input (str): The prompt or question given to the model.
            - model_output (str): The response generated by the model.
            - evaluation_criteria (str): The criteria for evaluation.
            - expected_model_output (Optional[str]): A reference answer (if available).
            - model_context (Optional[str]): Additional context for the model.
            - model_id (str): The Atla model ID to use for evaluation.

    Returns:
        List[Dict[str, str]]: A list of dictionaries, each containing the evaluation results:
            - "score": The numerical evaluation score.
            - "critique": A textual explanation of the evaluation.
    """
    tasks = [evaluate_response(**eval_req) for eval_req in evaluations]
    results = await asyncio.gather(*tasks)
    return results

@mcp.tool()
def list_metrics() -> List[Dict[str, str]]:
    """
    List available metrics using Atla's SDK.

    This function retrieves a list of available metrics from the Atla API.
    Each metric is returned as a dictionary containing its properties.

    Returns:
        List[Dict[str, str]]: A list of dictionaries, each representing a metric with the following keys:
            - "id": The unique identifier of the metric.
            - "name": The name of the metric.
            - "description": A brief description of what the metric measures or evaluates.
    """
    metrics = atla_client.metrics.list().metrics
    return [{"id": m.id, "name": m.name, "description": m.description} for m in metrics]

@mcp.tool()
def create_metric(
    name: str,
    metric_type: str,
    prompt: str,
    description: Optional[str] = None
) -> str:
    """
    Create a new custom metric using Atla's SDK.

    This function creates a new metric with the specified parameters, adds a prompt,
    and sets it as the active version. It returns the ID of the newly created metric.

    Args:
        name (str): The name of the new metric.
        metric_type (str): The type of the metric (e.g., "likert_1_to_5" or "likert_0_to_1").
        prompt (str): The evaluation prompt or instructions for using this metric.
        description (Optional[str]): A brief description of what the metric measures. Defaults to None.

    Returns:
        str: The unique identifier (ID) of the newly created metric.
    """
    # Step 1: Create the metric
    result = atla_client.metrics.create(
        name=name,
        metric_type=metric_type,
        description=description
    )
    metric_id = result.metric_id

    # Step 2: Add a prompt
    atla_client.metrics.prompts.create(
        metric_id=metric_id,
        content=prompt
    )

    # Step 3: Set the prompt version
    atla_client.metrics.prompts.set_active_prompt_version(
        metric_id=metric_id,
        version=1
    )

    return metric_id

@mcp.tool()
def get_metric_by_name(name: str) -> Dict[str, str]:
    """
    Retrieve a metric by its name using Atla's SDK.

    This function searches for a metric with the given name in the list of available metrics.
    If found, it returns the metric's details; otherwise, it raises a ValueError.

    Args:
        name (str): The name of the metric to retrieve.

    Returns:
        Dict[str, str]: A dictionary containing the metric's details:
            - "id": The unique identifier of the metric.
            - "name": The name of the metric.
            - "description": A brief description of what the metric measures.

    Raises:
        ValueError: If a metric with the given name is not found.
    """
    # 1. Get the list of metrics and check if the metric exists
    metrics = list_metrics()
    metric = next((m for m in metrics if m["name"] == name), None)
    if not metric:
        raise ValueError(f"Metric with name '{name}' not found.")
    return metric

# Create an ASGI app for SSE transport instead of stdio
app = mcp.sse_app()

if __name__ == "__main__":
    logger.info("Starting Atla MCP server...")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")