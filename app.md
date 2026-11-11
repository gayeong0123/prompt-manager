import json
import os

DATA_FILE = "prompts.json"


def load_prompts():
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
            return []
    except json.JSONDecodeError:
        return []


def save_prompts(prompts):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(prompts, file, ensure_ascii=False, indent=4)


def get_next_id(prompts):
    if not prompts:
        return 1
    return max(prompt.get("id", 0) for prompt in prompts) + 1


def print_prompt(prompt):
    print("-" * 40)
    print(f"ID: {prompt.get('id')}")
    print(f"제목: {prompt.get('title')}")
    print(f"내용: {prompt.get('content')}")
    print(f"카테고리: {prompt.get('category')}")
    print(f"태그: {', '.join(prompt.get('tags', []))}")


def add_prompt(prompts):
    print("\n--- 새 프롬프트 추가 ---")

    title = input("제목: ").strip()

    # ✅ 1. 빈 값 검사 (제목 입력 직후)
    if not title:
        print("제목은 반드시 입력해야 합니다.")
        return

    # ✅ 2. 중복 검사 (제목 입력 직후)
    for prompt in prompts:
        if prompt.get("title", "").lower() == title.lower():
            print(f"❌ '{title}' 제목이 이미 존재합니다. 다른 제목을 사용하세요.")
            return

    # ✅ 3. 나머지 입력은 검사 통과 후에 받기
    content = input("내용: ").strip()

    if not content:
        print("내용은 반드시 입력해야 합니다.")
        return

    category = input("카테고리: ").strip()
    tags_input = input("태그(쉼표로 구분): ").strip()
    tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]

    prompt = {
        "id": get_next_id(prompts),
        "title": title,
        "content": content,
        "category": category,
        "tags": tags
    }

    prompts.append(prompt)
    save_prompts(prompts)

    print("✅ 프롬프트가 저장되었습니다.")


def show_all_prompts(prompts):
    print("\n--- 전체 목록 보기 ---")

    if not prompts:
        print("저장된 프롬프트가 없습니다.")
        return

    for prompt in prompts:
        print_prompt(prompt)


def search_prompts(prompts):
    print("\n--- 프롬프트 검색 ---")

    keyword = input("검색할 키워드(제목/내용): ").strip()

    if not keyword:
        print("검색어를 입력해야 합니다.")
        return

    results = []

    for prompt in prompts:
        title = prompt.get("title", "")
        content = prompt.get("content", "")

        if keyword.lower() in title.lower() or keyword.lower() in content.lower():
            results.append(prompt)

    if not results:
        print("검색 결과가 없습니다.")
        return

    print(f"검색 결과 {len(results)}개:")
    for prompt in results:
        print_prompt(prompt)


def update_prompt(prompts):
    print("\n--- 프롬프트 수정 ---")

    if not prompts:
        print("수정할 프롬프트가 없습니다.")
        return

    show_all_prompts(prompts)

    try:
        prompt_id = int(input("수정할 프롬프트 ID: ").strip())
    except ValueError:
        print("ID는 숫자로 입력해야 합니다.")
        return

    target = None
    for prompt in prompts:
        if prompt.get("id") == prompt_id:
            target = prompt
            break

    if target is None:
        print("해당 ID의 프롬프트를 찾을 수 없습니다.")
        return

    print("수정하지 않을 항목은 엔터만 누르세요.")

    new_title = input(f"새 제목({target.get('title')}): ").strip()
    new_content = input(f"새 내용({target.get('content')}): ").strip()
    new_category = input(f"새 카테고리({target.get('category')}): ").strip()
    new_tags = input(f"새 태그({', '.join(target.get('tags', []))}): ").strip()

    if new_title:
        target["title"] = new_title
    if new_content:
        target["content"] = new_content
    if new_category:
        target["category"] = new_category
    if new_tags:
        target["tags"] = [tag.strip() for tag in new_tags.split(",") if tag.strip()]

    save_prompts(prompts)

    print("프롬프트가 수정되었습니다.")


def delete_prompt(prompts):
    print("\n--- 프롬프트 삭제 ---")

    if not prompts:
        print("삭제할 프롬프트가 없습니다.")
        return

    show_all_prompts(prompts)

    try:
        prompt_id = int(input("삭제할 프롬프트 ID: ").strip())
    except ValueError:
        print("ID는 숫자로 입력해야 합니다.")
        return

    for prompt in prompts:
        if prompt.get("id") == prompt_id:
            confirm = input("정말 삭제하시겠습니까? (y/n): ").strip().lower()

            if confirm == "y":
                prompts.remove(prompt)
                save_prompts(prompts)
                print("프롬프트가 삭제되었습니다.")
            else:
                print("삭제가 취소되었습니다.")
            return

    print("해당 ID의 프롬프트를 찾을 수 없습니다.")


def filter_by_category_or_tag(prompts):
    print("\n--- 카테고리/태그별 조회 ---")

    if not prompts:
        print("저장된 프롬프트가 없습니다.")
        return

    keyword = input("조회할 카테고리 또는 태그: ").strip()

    if not keyword:
        print("조회할 값을 입력해야 합니다.")
        return

    results = []

    for prompt in prompts:
        category = prompt.get("category", "")
        tags = prompt.get("tags", [])

        if keyword.lower() == category.lower():
            results.append(prompt)
        elif any(keyword.lower() == tag.lower() for tag in tags):
            results.append(prompt)

    if not results:
        print("해당 카테고리 또는 태그의 프롬프트가 없습니다.")
        return

    print(f"조회 결과 {len(results)}개:")
    for prompt in results:
        print_prompt(prompt)


def toggle_favorite(prompts):
    print("\n--- 즐겨찾기 설정/해제 ---")

    if not prompts:
        print("저장된 프롬프트가 없습니다.")
        return

    show_all_prompts(prompts)

    try:
        prompt_id = int(input("즐겨찾기 설정/해제할 프롬프트 ID: ").strip())
    except ValueError:
        print("ID는 숫자로 입력해야 합니다.")
        return

    for prompt in prompts:
        if prompt.get("id") == prompt_id:
            # 현재 즐겨찾기 상태를 반대로 바꿈 (True→False, False→True)
            current = prompt.get("favorite", False)
            prompt["favorite"] = not current

            if prompt["favorite"]:
                print("⭐ 즐겨찾기에 추가되었습니다.")
            else:
                print("☆ 즐겨찾기가 해제되었습니다.")

            save_prompts(prompts)
            return

    print("해당 ID의 프롬프트를 찾을 수 없습니다.")


def show_favorites(prompts):
    print("\n--- 즐겨찾기 목록 ---")

    # favorite이 True인 것만 골라냄
    favorites = [p for p in prompts if p.get("favorite", False)]

    if not favorites:
        print("즐겨찾기한 프롬프트가 없습니다.")
        return

    print(f"즐겨찾기 {len(favorites)}개:")
    for prompt in favorites:
        print_prompt(prompt)


def export_to_txt(prompts):
    print("\n--- 텍스트 파일로 내보내기 ---")

    if not prompts:
        print("내보낼 프롬프트가 없습니다.")
        return

    filename = input("저장할 파일명 입력(예: export.txt): ").strip()

    if not filename:
        filename = "export.txt"

    if not filename.endswith(".txt"):
        filename += ".txt"

    with open(filename, "w", encoding="utf-8") as file:
        file.write("프롬프트 목록\n")
        file.write("=" * 40 + "\n\n")

        for prompt in prompts:
            file.write(f"ID: {prompt.get('id')}\n")
            file.write(f"제목: {prompt.get('title')}\n")
            file.write(f"내용: {prompt.get('content')}\n")
            file.write(f"카테고리: {prompt.get('category')}\n")
            file.write(f"태그: {', '.join(prompt.get('tags', []))}\n")
            file.write("-" * 40 + "\n")

    print(f"{filename} 파일로 내보내기 완료")


def show_menu():
    print("\n--- 🚀 프롬프트 관리 콘솔 ---")
    print("1. 새 프롬프트 추가")
    print("2. 전체 목록 보기")
    print("3. 프롬프트 검색")
    print("4. 프롬프트 수정")
    print("5. 프롬프트 삭제")
    print("6. 카테고리/태그별 조회")
    print("7. 즐겨찾기 설정/해제")
    print("8. 즐겨찾기 목록 보기")
    print("9. 텍스트 파일로 내보내기")
    print("10. 종료")


def main():
    prompts = load_prompts()

    while True:
        show_menu()
        choice = input("메뉴를 선택하세요 (1-10): ").strip()

        if choice == "1":
            add_prompt(prompts)
        elif choice == "2":
            show_all_prompts(prompts)
        elif choice == "3":
            search_prompts(prompts)
        elif choice == "4":
            update_prompt(prompts)
        elif choice == "5":
            delete_prompt(prompts)
        elif choice == "6":
            filter_by_category_or_tag(prompts)
        elif choice == "7":
            toggle_favorite(prompts)
        elif choice == "8":
            show_favorites(prompts)
        elif choice == "9":
            export_to_txt(prompts)
        elif choice == "10":
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 입력입니다. 1부터 10까지의 숫자를 입력하세요.")


if __name__ == "__main__":
    main()
