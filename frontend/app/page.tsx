import PizzaMap from "./components/PizzaMap";
import { Pizzeria } from "./types";

async function getPizzerias(): Promise<Pizzeria[]> {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
  const res = await fetch(`${apiUrl}/pizzerias`, {
    cache: "no-store",
  });

  if (!res.ok) {
    return [];
  }

  return res.json();
}

export default async function Home() {
  const pizzerias = await getPizzerias();

  return (
    <div className="flex min-h-screen flex-col bg-zinc-50 font-sans dark:bg-black">
      {/* Map section - 25% of viewport height */}
      <div className="h-[25vh] w-full">
        <PizzaMap pizzerias={pizzerias} />
      </div>

      {/* Content section */}
      <div className="flex-1 p-4">
        <h1 className="mb-4 text-2xl font-bold text-zinc-900 dark:text-white">
          Pizza Blog Berlin
        </h1>
        <p className="text-zinc-600 dark:text-zinc-400">
          {pizzerias.length} pizzerias visited
        </p>
      </div>
    </div>
  );
}
