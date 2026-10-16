// Manually authored illustration; not executed or verified.
export interface RegisterCustomerCommand {
  email?: string;
}
export interface TransactionScope { readonly context: unknown; }
export interface UnitOfWork {
  withinTransaction<T>(operation: (scope: TransactionScope) => Promise<T>): Promise<T>;
}
export class RegisterCustomerHandler {
  constructor(private readonly unitOfWork: UnitOfWork) {}
  async execute(command: RegisterCustomerCommand): Promise<void> {
    return this.unitOfWork.withinTransaction(async (scope) => {
      await this.applyBusinessRules(command, scope);
    });
  }
  private async applyBusinessRules(command: RegisterCustomerCommand, scope: TransactionScope): Promise<void> {
    // TODO: domain rules and persistence using scope.context.
    throw new Error("Business logic extension point is not implemented");
  }
}
