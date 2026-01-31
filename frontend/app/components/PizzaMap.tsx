"use client";

import { useState, useCallback, useEffect } from "react";
import {
  APIProvider,
  Map,
  AdvancedMarker,
  Pin,
  useMap,
} from "@vis.gl/react-google-maps";
import { Pizzeria } from "../types";

interface PizzaMapProps {
  pizzerias: Pizzeria[];
}

const BERLIN_CENTER = { lat: 52.52, lng: 13.405 };

function MapContent({
  pizzerias,
  selectedId,
  onSelect,
}: {
  pizzerias: Pizzeria[];
  selectedId: number | null;
  onSelect: (pizzeria: Pizzeria) => void;
}) {
  const map = useMap();
  const pizzeriasWithLocation = pizzerias.filter((p) => p.location !== null);

  // Fit bounds to show all markers on initial load
  useEffect(() => {
    if (!map || pizzeriasWithLocation.length === 0) return;

    const bounds = new google.maps.LatLngBounds();
    pizzeriasWithLocation.forEach((p) => {
      bounds.extend(p.location!);
    });
    map.fitBounds(bounds, { top: 20, right: 20, bottom: 20, left: 20 });
  }, [map, pizzeriasWithLocation]);

  // Pan to selected marker
  useEffect(() => {
    if (!map || !selectedId) return;

    const selected = pizzeriasWithLocation.find((p) => p.id === selectedId);
    if (selected?.location) {
      map.panTo(selected.location);
      map.setZoom(15);
    }
  }, [map, selectedId, pizzeriasWithLocation]);

  return (
    <>
      {pizzeriasWithLocation.map((pizzeria) => {
        const isSelected = pizzeria.id === selectedId;
        return (
          <AdvancedMarker
            key={pizzeria.id}
            position={pizzeria.location!}
            title={pizzeria.name}
            onClick={() => onSelect(pizzeria)}
          >
            <Pin
              background={isSelected ? "#3b82f6" : "#ef4444"}
              borderColor={isSelected ? "#1d4ed8" : "#b91c1c"}
              glyphColor={isSelected ? "#1d4ed8" : "#b91c1c"}
            />
          </AdvancedMarker>
        );
      })}
    </>
  );
}

export default function PizzaMap({ pizzerias }: PizzaMapProps) {
  const [selectedPizzeria, setSelectedPizzeria] = useState<Pizzeria | null>(
    null
  );
  const apiKey = process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY;

  const handleSelect = useCallback((pizzeria: Pizzeria) => {
    setSelectedPizzeria(pizzeria);
  }, []);

  if (!apiKey) {
    return (
      <div className="flex h-full w-full items-center justify-center bg-zinc-200 dark:bg-zinc-800">
        <p className="text-zinc-500">Google Maps API key not configured</p>
      </div>
    );
  }

  return (
    <div className="flex h-full w-full flex-col">
      <div className="flex-1">
        <APIProvider apiKey={apiKey}>
          <Map
            defaultCenter={BERLIN_CENTER}
            defaultZoom={12}
            mapId="pizza-map"
            className="h-full w-full"
            gestureHandling="greedy"
          >
            <MapContent
              pizzerias={pizzerias}
              selectedId={selectedPizzeria?.id ?? null}
              onSelect={handleSelect}
            />
          </Map>
        </APIProvider>
      </div>

      {/* Selected pizzeria display */}
      <div className="bg-white px-4 py-2 dark:bg-zinc-900">
        {selectedPizzeria ? (
          <p className="font-medium text-zinc-900 dark:text-white">
            {selectedPizzeria.name}
          </p>
        ) : (
          <p className="text-zinc-400">Click a marker to select a pizzeria</p>
        )}
      </div>
    </div>
  );
}
