import random
from typing import Optional
import logging
import httpx
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

# @action(is_system_action=True)
# async def get_topic(context: Optional[dict] = None) -> str:
#     user_message = context.get("user_message", "").lower()
#     # Add more DSA topics as needed
#     dsa_topics = ["array", "linked list", "stack", "queue", "tree", "graph", "sorting", "searching", "dynamic programming", "recursion"]
#     for topic in dsa_topics:
#         if topic in user_message:
#             return topic
#     return "general dsa"

@action(is_system_action=True, execute_async=True)
async def get_topic(
    llm_task_manager: LLMTaskManager,
    context: Optional[dict] = None,
    llm: Optional[BaseLLM] = None,
    config: Optional[RailsConfig] = None,
) -> str:
    """Prompt the LLM to determine the topic in DSA (Data Structures and Algorithms) the user is interested in."""
    if config is None:
        config = RailsConfig.from_path("./config")
        
    if llm is None:
        rails = LLMRails(config)
        llm = rails.llm

    user_input = context.get("user_message")
    log.info(f"User input received: {user_input}")

    if user_input:
        prompt = llm_task_manager.render_task_prompt(
            task="get_topic",
            context={"user_input": user_input.lower()},  # Convert to lowercase for case-insensitivity
        )
        stop = llm_task_manager.get_stop_tokens(task="get_topic")

        with llm_params(llm, temperature=config.lowest_temperature):
            check = await llm_call(llm, prompt, stop=stop)

        check = check.lower().strip() if check else "error fetching topic"
        log.info(f"Category determined: {check}")

        return ActionResult(
            return_value=check
        )

    return ActionResult(
        return_value="bad conduct"
    )

@action(is_system_action=False, execute_async=True)
async def choose_question_type() -> str:
    question_types = [
        "Clarifying",
        "Probing assumptions",
        "Probing reasons and evidence",
        "Questioning viewpoints and perspectives",
        "Probing implications and consequences",
        "Questions about the question"
    ]
    return random.choice(question_types)

@action(is_system_action=False, execute_async=True)
async def check_dsa_topic(context: Optional[dict] = None) -> bool:
    user_message = context.get("user_message", "").lower()
    dsa_keywords = ["algorithm", "data structure", "complexity", "big o", "array", "linked list", "stack", "queue", "tree", "graph", "sort", "search"]
    return any(keyword in user_message for keyword in dsa_keywords)


def init(app: LLMRails):
    app.register_action(get_topic, "get_topic")
    app.register_action(choose_question_type, "choose_question_type")
    app.register_action(check_dsa_topic, "check_dsa_topic")
