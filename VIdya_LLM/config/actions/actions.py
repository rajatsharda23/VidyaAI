from typing import Optional
import logging
from nemoguardrails.actions import action
from nemoguardrails import LLMRails
from nemoguardrails.llm.taskmanager import LLMTaskManager
from langchain.llms.base import BaseLLM
from nemoguardrails import RailsConfig
from nemoguardrails.actions.actions import ActionResult, action
from nemoguardrails.actions.llm.utils import llm_call
from nemoguardrails.context import llm_call_info_var
from nemoguardrails.llm.params import llm_params


log = logging.getLogger(__name__)

@action(is_system_action=True, execute_async=True)
async def check_blocked_terms(context: Optional[dict] = None):
    
    bot_response = context.get("bot_message")

    # A quick hard-coded list of proprietary terms. You can also read this from a file.
    blocked_Terms = ["sharda", "gambhir"]

    for term in blocked_Terms:
        if term in bot_response.lower():
            return True
        
    return False



#Find Category Action! Asking the LLM the category the blocked message falls into
@action(is_system_action=True, execute_async=True)
async def find_category(
    llm_task_manager: LLMTaskManager,
    context: Optional[dict] = None,
    llm: Optional[BaseLLM] = None,
    config: Optional[RailsConfig] = None,
) -> str:
    """Prompt the LLM to determine the category that the user input belongs to."""

    if config is None:
        config = RailsConfig.from_path("./config")
        
    if llm is None:
        rails = LLMRails(config)
        llm = rails.llm

    user_input = context.get("user_message", "")
    log.info(f"User input received: {user_input}")

    if user_input:
        prompt = llm_task_manager.render_task_prompt(
            task="find_category",
            context={"user_input": user_input},
        )
        stop = llm_task_manager.get_stop_tokens(task="find_category")

        with llm_params(llm, temperature=config.lowest_temperature):
            result = await llm_call(llm, prompt, stop=stop)

        if result:
            log.info(f"Category determined: {result}")
        
        return ActionResult(return_value=result)
    
    return ActionResult(return_value="something went wrong....")

def init(app: LLMRails):
    app.register_action(find_category, "find_category")
    app.register_action(check_blocked_terms, "check_blocked_terms")

