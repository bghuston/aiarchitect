// Manually authored illustrative output; not executed or verified.
export interface Customer {
  id: string; // UUID supplied by the persistence boundary
  name: string;
  email: string;
  registeredAt?: Date;
  createdAt: Date;
  updatedAt: Date;
  deletedAt: Date | null;
}
