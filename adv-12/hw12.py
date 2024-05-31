from collections import deque
snake_queue=deque()
snake_queue.append("小名")
snake_queue.append("sb")
snake_queue.append("小強")
print(f"初始對列:{snake_queue}")
first_student=snake_queue.popleft()
print(f"{first_student}已經購買點心並離開對列")
print(f"現在的隊列:{snake_queue}")