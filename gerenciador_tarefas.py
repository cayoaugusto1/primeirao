import json
import os

class Task:
    def __init__(self, description, done=False):
        self.description = description
        self.done = done

    def to_dict(self):
        return {"description": self.description, "done": self.done}

    @staticmethod
    def from_dict(data):
        return Task(data['description'], data['done'])

class TaskManager:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as f:
                    data = json.load(f)
                    self.tasks = [Task.from_dict(t) for t in data]
            except (json.JSONDecodeError, IOError):
                print("Erro ao ler o arquivo de tarefas. Começando com lista vazia.")
                self.tasks = []
        else:
            self.tasks = []

    def save_tasks(self):
        with open(self.filename, "w") as f:
            json.dump([task.to_dict() for task in self.tasks], f, indent=4)

    def add_task(self, description):
        self.tasks.append(Task(description))
        self.save_tasks()
        print(f"Tarefa '{description}' adicionada.")

    def list_tasks(self):
        if not self.tasks:
            print("Nenhuma tarefa cadastrada.")
            return
        print("\nTarefas:")
        for i, task in enumerate(self.tasks, 1):
            status = "✔" if task.done else "✘"
            print(f"{i}. [{status}] {task.description}")

    def mark_done(self, task_number):
        if 1 <= task_number <= len(self.tasks):
            self.tasks[task_number-1].done = True
            self.save_tasks()
            print(f"Tarefa {task_number} marcada como concluída.")
        else:
            print("Número de tarefa inválido.")

    def remove_task(self, task_number):
        if 1 <= task_number <= len(self.tasks):
            removed = self.tasks.pop(task_number-1)
            self.save_tasks()
            print(f"Tarefa '{removed.description}' removida.")
        else:
            print("Número de tarefa inválido.")

def menu():
    print("\n=== GERENCIADOR DE TAREFAS ===")
    print("1 - Listar tarefas")
    print("2 - Adicionar tarefa")
    print("3 - Marcar tarefa como concluída")
    print("4 - Remover tarefa")
    print("0 - Sair")

def main():
    manager = TaskManager()

    while True:
        menu()
        choice = input("Escolha uma opção: ")

        if choice == "0":
            print("Saindo...")
            break

        elif choice == "1":
            manager.list_tasks()

        elif choice == "2":
            desc = input("Descrição da tarefa: ")
            if desc.strip():
                manager.add_task(desc.strip())
            else:
                print("Descrição inválida.")

        elif choice == "3":
            try:
                num = int(input("Número da tarefa para marcar como concluída: "))
                manager.mark_done(num)
            except ValueError:
                print("Digite um número válido.")

        elif choice == "4":
            try:
                num = int(input("Número da tarefa para remover: "))
                manager.remove_task(num)
            except ValueError:
                print("Digite um número válido.")

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()