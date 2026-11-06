prompts = [
    {
        "id": 1,
        "title": "블로그 글쓰기",
        "category": "writing",
        "content": "친절하고 읽기 쉬운 블로그 글을 작성해줘.",
        "favorite": True
    },
    {
        "id": 2,
        "title": "영어 번역",
        "category": "translation",
        "content": "자연스러운 영어로 번역해줘.",
        "favorite": False
    },
    {
        "id": 3,
        "title": "코드 설명",
        "category": "coding",
        "content": "초보자도 이해할 수 있게 코드 동작을 설명해줘.",
        "favorite": True
    }
]


def show_menu():
    print("\n=== 프롬프트 관리자 ===")
    print("1. 프롬프트 추가")
    print("2. 프롬프트 목록 보기")
    print("3. 카테고리별 보기")
    print("4. 검색하기")
    print("5. 상세 보기")
    print("6. 즐겨찾기 보기")
    print("7. 종료")


def add_prompt():
    print("\n[프롬프트 추가]")

    title = input("제목: ")
    category = input("카테고리: ")
    content = input("내용: ")
    favorite_input = input("즐겨찾기 여부 (y/n): ")

    if favorite_input.lower() == "y":
        favorite = True
    else:
        favorite = False

    new_id = len(prompts) + 1

    new_prompt = {
        "id": new_id,
        "title": title,
        "category": category,
        "content": content,
        "favorite": favorite
    }

    prompts.append(new_prompt)
    print("프롬프트가 추가되었습니다.")


def list_prompts():
    print("\n[프롬프트 목록]")

    if len(prompts) == 0:
        print("등록된 프롬프트가 없습니다.")
        return

    for prompt in prompts:
        print(f"{prompt['id']}. {prompt['title']} / {prompt['category']}")


def view_by_category():
    print("\n[카테고리별 보기]")
    category = input("카테고리 입력: ")

    found = False
    for prompt in prompts:
        if prompt["category"].lower() == category.lower():
            print(f"{prompt['id']}. {prompt['title']} / {prompt['category']}")
            found = True

    if not found:
        print("해당 카테고리의 프롬프트가 없습니다.")


def search_prompt():
    print("\n[검색하기]")
    keyword = input("검색어 입력: ")

    found = False
    for prompt in prompts:
        if keyword.lower() in prompt["title"].lower() or keyword.lower() in prompt["content"].lower():
            print(f"{prompt['id']}. {prompt['title']} / {prompt['category']}")
            found = True

    if not found:
        print("검색 결과가 없습니다.")


def view_detail():
    print("\n[상세 보기]")
    prompt_id = input("프롬프트 ID 입력: ")

    if not prompt_id.isdigit():
        print("숫자를 입력하세요.")
        return

    prompt_id = int(prompt_id)

    for prompt in prompts:
        if prompt["id"] == prompt_id:
            print(f"\nID: {prompt['id']}")
            print(f"제목: {prompt['title']}")
            print(f"카테고리: {prompt['category']}")
            print(f"내용: {prompt['content']}")
            print(f"즐겨찾기: {prompt['favorite']}")
            return

    print("해당 ID의 프롬프트가 없습니다.")


def view_favorites():
    print("\n[즐겨찾기 목록]")

    found = False
    for prompt in prompts:
        if prompt["favorite"]:
            print(f"{prompt['id']}. {prompt['title']} / {prompt['category']}")
            found = True

    if not found:
        print("즐겨찾기한 프롬프트가 없습니다.")


while True:
    show_menu()
    choice = input("메뉴 번호를 선택하세요: ")

    if choice == "1":
        add_prompt()
    elif choice == "2":
        list_prompts()
    elif choice == "3":
        view_by_category()
    elif choice == "4":
        search_prompt()
    elif choice == "5":
        view_detail()
    elif choice == "6":
        view_favorites()
    elif choice == "7":
        print("프로그램을 종료합니다.")
        break
    else:
        print("올바른 번호를 입력하세요.")