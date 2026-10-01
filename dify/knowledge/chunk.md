

# Performance
General mode
- chunk overlap: 10%-25% of max chunk size

Parent-Child
- 适用于精准查找
  - child chunk尺寸如果和关键词一样，就能达到1.00 score 匹配
- child chunk size: < 4000 tokens 
- parent chunk size: 
  - full_doc: < 10000 tokens
  - paragraph: < 4000 tokens

