export const recordUsers = (
  email: string
): Hooks.UseAccountTypes.IUser | undefined => {
  return mockUsers.find(user => user.email === email)
}

const mockUsers = [
  { email: 'chanel', name: 'Chanel' },
  { email: 'lucas.silva@ckl.io', name: 'Lucas Magnus' },
]
