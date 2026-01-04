from core.tracker_service import (
    add_question,
    get_today_tasks,
    mark_done,
    get_consistency,
    get_missed_days,
    get_weak_questions
)

while True:
    print("\n===== DSA TRACKER =====")
    print("1. Add Question")
    print("2. Show Today's Tasks")
    print("3. Mark Done")
    print("4. Show Consistency")
    print("5. Show Missed Days")
    print("6. Show Weak Questions")
    print("7. Exit")

    choice = input("> ").strip()

    if choice == "1":
        q = input("Question No: ").strip()
        d = input("Difficulty (easy/medium/hard): ").lower().strip()
        print(add_question(q, d))

    elif choice == "2":
        tasks = get_today_tasks()
        if not tasks:
            print("🎉 Nothing to do today")
        else:
            print("\n📅 TODAY'S TASKS")
            for q, d in tasks:
                print(f"- {q} ({d})")

    elif choice == "3":
        q = input("Question No: ").strip()
        print(mark_done(q))

    elif choice == "4":
        c = get_consistency()
        print("\n🔥 CONSISTENCY")
        print(f"Score          : {c['score']}%")
        print(f"Current Streak : {c['current_streak']}")
        print(f"Best Streak    : {c['max_streak']}")

    elif choice == "5":
        missed = get_missed_days()
        print("\n❌ MISSED DAYS")
        if not missed:
            print("🎉 No missed days!")
        else:
            for q, days in missed.items():
                print(f"{q} → {days}")

    elif choice == "6":
        weak = get_weak_questions()
        print("\n⚠️ WEAK QUESTIONS")
        if not weak:
            print("🎉 No weak questions!")
        else:
            for q, cnt in weak.items():
                print(f"{q} → missed {cnt} times")

    elif choice == "7":
        break

    else:
        print("❌ Invalid choice")
