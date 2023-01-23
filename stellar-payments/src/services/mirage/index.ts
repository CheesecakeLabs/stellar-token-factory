import { createServer, Server } from 'miragejs';
import { Mockups } from 'services/mockups';


export function makeServer({ environment }: { environment: 'dev' }): Server {
  const server = createServer({
    environment,

    routes() {
      this.timing = 2000

      this.get('/payees', () => {
        return Mockups.payees
      })
    },
  })

  return server
}