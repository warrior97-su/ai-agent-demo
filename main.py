import sys
from agent import Agent

def main():
    agent = Agent()
    if(len(sys.argv) > 1):
        question = " ".join(sys.argv[1:])
        agent.run(question)
        return 
    else:
        print("Agent 已启动，输入 quit 退出")
        while True:
            question = input("请输入问题: ")
            if question == "quit":
                print("Agent 已退出")
                break
            answer = agent.run(question)
if __name__ == "__main__":
    main()