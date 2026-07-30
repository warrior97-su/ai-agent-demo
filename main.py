import sys
from agent import Agent

def main():
    if(len(sys.argv) > 1):
        question = " ".join(sys.argv[1:])
    else:
        question = "哈尔滨天气怎么样？现在温度是多少？，顺便帮我算一下2*3的计算结果"
    agent = Agent()
    answer = agent.run(question)

if __name__ == "__main__":
    main()