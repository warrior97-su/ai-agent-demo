import sys

from agent import Agent


def main():
    agent = Agent()

    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
        agent.run(question)
        return

    print("Agent 已启动，输入 quit 退出")
    while True:
        question = input("\n你: ").strip()
        if not question:
            continue
        if question.lower() in ("quit", "exit", "q"):
            print("再见！")
            break
        agent.run(question)


if __name__ == "__main__":
    main()
