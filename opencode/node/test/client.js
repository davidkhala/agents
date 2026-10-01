import {Client} from '../index.js'
import assert from "assert";
describe('connect to local', function () {
    this.timeout(0)
    const client = new Client()
    it('healthcheck', async ()=> {
        assert.equal(await client.healthcheck(), '1.1.4')
    })
    it('log', async ()=> {
        await client.log('hello')
    })
    it('agents', async () =>{
        const r = await client.agents()
        console.log(r)
    })
    it('projects', async ()=>{
        console.log(await client.projects())
    })
    it('context',async ()=>{
        console.log(await client.context())
    })
    it('config', async ()=>{
        console.log(await client.config())
    })

})