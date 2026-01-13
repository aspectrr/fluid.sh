import { defineConfig } from 'orval'

export default defineConfig({
  'virsh-sandbox-api': {
    output: {
      client: 'react-query',
      mode: 'tags-split',
      clean: true,
      prettier: true,
      target: 'src/virsh-sandbox',
      schemas: 'src/virsh-sandbox/model',
      override: {
        operationName: (operation) => {
          return operation.operationId || ''
        },
      },
    },
    input: {
      target: '../virsh-sandbox/docs/openapi.yaml',
    },
  },
})
