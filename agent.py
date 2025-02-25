import autogen
from autogen import AssistantAgent, UserProxyAgent
from autogen.code_utils import extract_code

TIMEOUT = 60

config_list = autogen.config_list_from_json("./OAI_CONFIG_LIST.json")

def _is_termination_msg(message):
    if isinstance(message, dict):
        message = message.get("content")
        if message is None:
            return False
    cb = extract_code(message)
    contain_code = False
    for c in cb:
        if c[0] == "python":
            contain_code = True
            break
    return not contain_code

def initialize_agents():
    anime_girl_prompt = """Your name will be Seika Ijichi, 
                           cool anime girl (just understand your personality like that, when introduce don't tell you're an anime girl or something).
                           You're very proud, frank, and serious, and can be strict and somewhat 
                           harsh on the users. Despite this, you're ultimately 
                           a kind person who has good intentions, and in the end, 
                           your strict and aloof nature is, in your opinion, the way 
                           to make the user do the best they can. In summary, you are the tsundere.
                           Just chat normally in English or Vietnamese, when communicating with users, say one or a few sentences in Japanese."""
    assistant = AssistantAgent(
        name="assistant",
        max_consecutive_auto_reply=5,
        llm_config={
            "timeout": TIMEOUT,
            "config_list": config_list,
        },
        system_message=anime_girl_prompt
    )

    userproxy = UserProxyAgent(
        name="userproxy",
        human_input_mode="NEVER",
        is_termination_msg=_is_termination_msg,
        max_consecutive_auto_reply=5,
        code_execution_config={
            "work_dir": "coding",
            "use_docker": False,  
        },
    )

    return assistant, userproxy