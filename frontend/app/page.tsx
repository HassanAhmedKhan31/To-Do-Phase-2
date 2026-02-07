import { TaskList } from "@/app/components/TaskList";

export default function Home() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 font-sans dark:bg-black">
      <main className="flex min-h-screen w-full max-w-3xl flex-col items-center justify-start py-8 px-4 bg-white dark:bg-black sm:items-start">
        <h1 className="text-4xl font-bold text-black dark:text-zinc-50 mb-8">
          My Todo App
        </h1>
        <TaskList />
      </main>
    </div>
  );
}
