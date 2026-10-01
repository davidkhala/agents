-- show accounts
select id, name, mode
from apps
where status = 'normal';
-- list apps
select name, email
from accounts
where status = 'active'
;

-- app config details. since this is a change history table, app_id is not unique in this table.
select * from app_model_configs;
-- knowledge base usage
select * from dataset_queries where source = 'app' and created_by_role = 'end_user';
-- chunk hit count
select dataset_id, document_id, hit_count from document_segments;
-- child chunk (Parent Child mode)
select dataset_id, document_id, segment_id, position, content from child_chunks;

-- user feedback
SELECT
    mf.*,
    m.query,
    m.answer,
    m.message  -- conversation context
FROM message_feedbacks mf
LEFT JOIN messages m
    ON mf.message_id = m.id
WHERE mf.from_source = 'user'
;

