import {createOpencode, createOpencodeClient} from "@opencode-ai/sdk"
import {createOpencodeClient as v2Client} from "@opencode-ai/sdk/v2"
import assert from "assert"

export async function run(port, host) {
    const {client, server} = await createOpencode({
        host: host,
        port: port,
    })
    return [server, client]
}

export class Client {
    constructor({
                    protocol = 'http',
                    host = 'localhost',
                    port = 4096,
                } = {}) {
        this.baseUrl = `${protocol}://${host}:${port}`
        this.client = createOpencodeClient({
            baseUrl: this.baseUrl,
        })
        this.logGroup = ''
    }


    async healthcheck() {
        const client = new v2Client({
            baseUrl: this.baseUrl
        })
        const {data, error} = await client.global.health()

        if (error) {
            assert.ok(!data)
            if (!(error instanceof TypeError))throw error
            return
        }

        const {healthy, version} = data
        assert.ok(healthy)
        return version
    }

    async agents() {
        const {data} = await this.client.app.agents()
        return data
    }

    /**
     *
     * @param {string} message
     * @param {string} [level]
     */
    async log(message, level = 'info') {

        const {data} = await this.client.app.log({
            body: {
                service: this.logGroup,
                level: level,
                message: message,
            },
        })
        assert.ok(data)
    }
    async projects(){
        const {data} = await this.client.project.list()
        return data
    }


    async context(){
        const {data: project} = await this.client.project.current()
        const {data: path} = await this.client.path.get()
        return {project, path}
    }
    async config(){
        const {data: config} = await this.client.config.get()
        const { providers, default: defaults } = await this.client.config.providers()
        // TODO what are defaults?
        return {config, providers}
    }

}