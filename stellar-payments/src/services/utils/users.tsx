export const recordUsers = (
  email: string
): Hooks.UseAccountTypes.IUser | undefined => {
  return mockUsers.find(user => user.email === email)
}

const mockUsers = [
  { email: 'john', name: 'John' },
  { email: 'jane', name: 'Jane' },
  { email: 'amy', name: 'Amy' },
]
