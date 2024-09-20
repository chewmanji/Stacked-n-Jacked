import { Exercise } from "../lib/definitions";

export default function Page(exercise: Exercise) {
  return <p>{exercise.name}</p>;
}
