# Knowledge Pipeline
> You can now convert your existing knowledge base to use the Knowledge Pipeline for document processing 
- Covert cannot be undone
- allow access to plugins from Dify marketplace

## Input field
type `Short Text`
- Max Length: 256

type `Paragraph`
- bug: limit up to 48 length. And not editable

# Documents
sync
- sync will rerun the process of embedding
- overwrite: existing modification on chunks will be lost
- for general document only
  - raise error if converted to rag-workflow 

# Dataset 
Native Data source
- import from file
  - Max 5 in a batch
  - Max 15 MB each file
- Sync from Notion
- Sync from website (crawler)
  - Jina Reader: 20 subpages
    - cannot read this page
    - dedup: for different urls under same domain, top 20 Subpages is always the same  
  - Firecrawl
    - good at read current page


provision only
- Notion and website data source cannot be used after provision.
  - solution:　convert this dataset to pipeline mode 

Text search bar for finding a document is case-sensitive to your query

name is not unique: different documents can have same name