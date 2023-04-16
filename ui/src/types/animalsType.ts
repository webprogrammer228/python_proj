export type genderType = {
  gender: "MALE" | "FEMALE" | "OTHER";
};

export type animal = {
  chipperId: number;
  chippingDateTime: string;
  chippingLocationId: number;
  deathDateTime: null | string;
  gender: string;
  height: number;
  id: number;
  length: number;
  lifeStatus: "ALIVE" | "DEAD";
  visitedLocations: number[];
  weight: number;
};

export type animalType = {
  id: number;
  type: string;
};

export type newAnimalType = {
  animalTypes: number[];
  weight: number;
  length: number;
  height: number;
  gender: string;
  chipperId: number;
  chippingLocationId: number;
};
