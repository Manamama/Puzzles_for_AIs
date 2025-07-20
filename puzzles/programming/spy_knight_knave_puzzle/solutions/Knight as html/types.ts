
export type Role = 'knight' | 'knave' | 'spy';
export type Person = 'A' | 'B' | 'C';
export type RolesMap = Record<Person, Role>;

export interface VerificationResult {
  id: number;
  permutation: RolesMap;
  log: { message: string; isConsistent: boolean }[];
  isSolution: boolean;
}
