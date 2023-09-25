from awq import AutoAWQForCausalLM
from transformers import AutoTokenizer
from llama_out import format_the_output


def idea_generator(prompt:str, repo:str):
    model = AutoAWQForCausalLM.from_quantized(repo, fuse_layers=True, trust_remote_code=False, safetensors=True)                                  
    tokenizer = AutoTokenizer.from_pretrained(repo, trust_remote_code=False)
    users_prompt = prompt
    prompt = f"Make a concept for an artwork to draw. Concept must be 30-40 words long. Concept theme is {users_prompt}"
    prompt_template=f'''[INST] <<SYS>>
    You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe.  Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature. If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.
    <</SYS>>
    {prompt}[/INST]
    '''
    tokens = tokenizer(prompt_template, return_tensors='pt').input_ids.cuda()
    generation_output = model.generate(tokens, do_sample=True, temperature=0.7, top_p=0.95, top_k=40, max_new_tokens=512)
    formatted_output = format_the_output(tokenizer.decode(generation_output[0]))
    return formatted_output