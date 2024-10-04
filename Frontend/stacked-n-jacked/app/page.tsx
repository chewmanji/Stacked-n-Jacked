import { HomePageButtons } from "./ui/dashboard-button";
import { ModeToggle } from "./ui/mode-toggle";

export default async function Home() {
  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20">
      <main className="flex flex-col gap-8 row-start-2 items-center sm:items-start">
        <p className="font-bold text-xl">Stacked&Jacked</p>
        <div className="flex gap-4 items-center flex-col sm:flex-row">
          Start tracking your gains today!
          <HomePageButtons />
          <ModeToggle />
        </div>
      </main>
      <footer className="row-start-3 flex gap-6 flex-wrap items-center justify-center"></footer>
    </div>
  );
}
