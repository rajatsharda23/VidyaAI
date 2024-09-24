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
from .socraticActions import get_topic, choose_question_type, check_dsa_topic

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
@action(is_system_action=True)
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


    print('------------------------------------------------------------------------')
    print('FIND_CATEGORY WAS CALLED')
    print('------------------------------------------------------------------------')

    user_input = context.get("user_message")
    log.info(f"User input received: {user_input}")

    if user_input:
        prompt = llm_task_manager.render_task_prompt(
            task="find_category",
            context={"user_input": user_input.lower()},  # Convert to lowercase for case-insensitivity
        )
        stop = llm_task_manager.get_stop_tokens(task="find_category")

        with llm_params(llm, temperature=config.lowest_temperature):
            check = await llm_call(llm, prompt, stop=stop)

        check = check.lower().strip() if check else "error fetching category"
        log.info(f"Category determined: {check}")

        print('------------------------------------------------------------------------')
        print(f'category found----> ', check)
        print('------------------------------------------------------------------------')
        

        return ActionResult(
            return_value=check
        )

    return ActionResult(
        return_value="Bad manners"
    )

def init(app: LLMRails):
    app.register_action(find_category, "find_category")
    app.register_action(check_blocked_terms, "check_blocked_terms")
    app.register_action(get_topic, "get_topic")
    app.register_action(choose_question_type, "choose_question_type")
    app.register_action(check_dsa_topic, "check_dsa_topic")
