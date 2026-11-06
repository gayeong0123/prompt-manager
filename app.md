import json
import os
from datetime import datetime

# 데이터 파일 경로
DATA_FILE = "prompts.json"

def load_data():
    """파일에서 데이터를 불러옵니다."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_data(prompts):
    """파일에 데이터를 저장합니다."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(prompts, f, ensure_ascii=False, indent=4)

def get_next_id(prompts):
    """새로운 ID를 생성합니다 (가장 큰 ID + 1)."""
    if not prompts:
        return 1
    return max(p['id'] for p in prompts) + 1

def main():
    prompts = load_data()

    while True:
        print("\n--- 🚀 프롬프트 관리 콘솔 ---")
        print("1. 새 프롬프트 추가")
        print("2. 전체 목록 보기")
        print("3. 프롬프트 검색")
        print("4. 프롬프트 수정")
        print("5. 프롬프트 삭제")
        print("6. 텍스트 파일로 내보내기")
        print("7. 종료")
        
        choice = input("메뉴를 선택하세요 (1-7): ")

        if choice == '1':
            title = input("제목: ")
            content = input("내용: ")
            tags = input("태그 (쉼표로 구분): ").split(',')
            new_prompt = {
                "id": get_next_id(prompts),
                "title": title,
                "content": content,
                "tags": [tag.strip() for tag in tags],
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            prompts.append(new_prompt)
            save_data(prompts)
            print("✅ 저장되었습니다!")

        elif choice == '2':
            print("\n--- 프롬프트 목록 ---")
            for p in prompts:
                print(f"[{p['id']}] {p['title']} ({p['date']})")

        elif choice == '3':
            keyword = input("검색할 키워드(제목/내용): ")
            results = [p for p in prompts if keyword in p['title'] or keyword in p['content']]
            for p in results:
                print(f"\nID: {p['id']}\n제목: {p['title']}\n내용: {p['content']}")

        elif choice == '4':
            target_id = int(input("수정할 프롬프트 ID: "))
            for p in prompts:
                if p['id'] == target_id:
                    p['title'] = input(f"새 제목 ({p['title']}): ") or p['title']
                    p['content'] = input(f"새 내용 ({p['content']}): ") or p['content']
                    save_data(prompts)
                    print("✅ 수정 완료!")
                    break

        elif choice == '5':
            target_id = int(input("삭제할 프롬프트 ID: "))
            prompts = [p for p in prompts if p['id'] != target_id]
            save_data(prompts)
            print("✅ 삭제 완료!")

        elif choice == '6':
            with open("prompts_export.txt", "w", encoding="utf-8") as f:
                for p in prompts:
                    f.write(f"ID: {p['id']}\n제목: {p['title']}\n내용: {p['content']}\n{'-'*20}\n")
            print("✅ prompts_export.txt로 저장되었습니다!")

        elif choice == '7':
            print("프로그램을 종료합니다. 안녕히 가세요!")
            break
        else:
            print("❌ 잘못된 선택입니다. 다시 입력해주세요.")

if __name__ == "__main__":
    main()
