export interface Location {
  lat: number;
  lng: number;
}

export interface Pizzeria {
  id: number;
  name: string;
  address: string;
  location: Location | null;
  rating: number | null;
  google_maps_url: string | null;
  review: string | null;
  visited_at: string | null;
  created_at: string;
  updated_at: string;
}
