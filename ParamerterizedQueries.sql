
-- Generated with help from Gemini

-- USERS TABLE

-- Insert a new user
INSERT
INTO users
  (email, password)
VALUES
  (%s, %s)
RETURNING
  id,
  email,
  user_type,
  tokens;

-- Select a user by email
SELECT
  id, email, password,
  user_type, tokens
FROM
  users
WHERE
  email = %s;

-- Select a user by ID
SELECT
  id, email, user_type, tokens
FROM
  users
WHERE
  id = %s;

-- Update user tokens
UPDATE
  users
SET
  tokens = %s
WHERE
  id = %s;

-- Update user type
UPDATE
  users
SET
  user_type = %s
WHERE
  id = %s;

--|----------------------------------------------------------------------------|

-- UserPosts TABLE

-- Insert a new user post
INSERT
INTO
"UserPosts" (
  "UserId",
  "DocumentId",
  "Payload"
)
VALUES
  (%s, %s, %s)
RETURNING
  "PostId",
  "CreationDate",
  "State";

-- Select a user post by PostId
SELECT
  "PostId",
  "UserId",
  "DocumentId",
  "CreationDate",
  "State",
  "Payload"
FROM
  "UserPosts"
WHERE "PostId" = %s;

-- Select all posts for a given DocumentId
SELECT
  "PostId",
  "UserId",
  "CreationDate",
  "State",
  "Payload"
FROM
  "UserPosts"
WHERE
  "DocumentId" = %s
ORDER BY
  "CreationDate" ASC;

-- Update the state of a user post
UPDATE
  "UserPosts"
SET
  "State" = %s
WHERE
  "PostId" = %s;

-- Update the payload of a user post
UPDATE
  "UserPosts"
SET
  "Payload" = %s
WHERE
  "PostId" = %s;

--|----------------------------------------------------------------------------|

-- DOCUMENTS TABLE

-- Insert a new document
INSERT
  INTO documents
  (owner_id, title)
VALUES
  (%s, %s)
RETURNING
  id,
  created_at,
  updated_at;

-- Select a document by ID
SELECT
  id, owner_id, title, content, created_at, updated_at
FROM
  documents
WHERE
  id = %s;

-- Update a document's title
UPDATE
  documents
SET
  title = %s, updated_at = NOW()
WHERE
  id = %s;

-- Update a document's content
UPDATE
  documents
SET
  content = %s, updated_at = NOW()
WHERE
  id = %s;

--|----------------------------------------------------------------------------|

-- DocumentView (Note: Views themselves aren't directly parameterized in the same way,
-- but you would parameterize the query *against* the view)

-- Select posts for a specific DocumentId from the DocumentView
SELECT
  PostId, UserId, CreationDate, Payload
FROM
  "DocumentView"
WHERE
  UserId IN
  (SELECT
    "UserId"
   FROM
    "UserPosts"
   WHERE
    "DocumentId" = %s)
ORDER BY
  CreationDate ASC;

--|----------------------------------------------------------------------------|

-- DocumentAuthorization TABLE

-- Insert a new document authorization (grant access to a user for a document)
INSERT
  INTO "DocumentAuthorization"
    ("DocumentId", "UserId")
  VALUES
    (%s, %s);

-- Select all UserIds authorized for a specific DocumentId
SELECT
  "UserId"
FROM
  "DocumentAuthorization"
WHERE
  "DocumentId" = %s;

-- Check if a user is authorized for a specific DocumentId
SELECT 1
FROM
    "DocumentAuthorization"
WHERE
  "DocumentId" = %s AND
  "UserId" = %s;

-- Remove authorization for a user from a document
DELETE
FROM
  "DocumentAuthorization"
WHERE
  "DocumentId" = %s AND
  "UserId" = %s;

--|----------------------------------------------------------------------------|

-- CORRECTIONS TABLE

-- Insert a new correction
INSERT
  INTO corrections
    (document_id, user_id, type,
    original_text, corrected_text,
    tokens_used)
  VALUES
    (%s, %s, %s, %s, %s, %s)
  RETURNING
    id, created_at, status;

-- Select corrections for a specific document
SELECT
  id, user_id, type,
  original_text, corrected_text,
  status, tokens_used, created_at
  FROM
    corrections
  WHERE
    document_id = %s
  ORDER BY
    created_at DESC;

-- Update the status of a correction
UPDATE
  corrections
SET
  status = %s
WHERE
  id = %s;

--|----------------------------------------------------------------------------|

-- COMPLAINTS TABLE

-- Insert a new complaint
INSERT
INTO complaints
  (complainant_id, accused_id, document_id, reason)
VALUES
  (%s, %s, %s, %s)
RETURNING
  id, status, created_at;

-- Select complaints related to a specific document
SELECT
  id, complainant_id,
  accused_id, reason,
  status, created_at
FROM
  complaints
WHERE
  document_id = %s
ORDER BY
  created_at DESC;

-- Update the status of a complaint
UPDATE
  complaints
SET
  status = %s
WHERE
  id = %s;

--|----------------------------------------------------------------------------|

-- GenericRequests TABLE

-- Insert a new generic request
INSERT
INTO "GenericRequests"
  (requester_id, authorizer_id, request_type)
VALUES
  (%s, %s, %s)
RETURNING
  request_id, request_status, created_at;

-- Update the status of a generic request
UPDATE
"GenericRequests"
SET request_status = %s
WHERE request_id = %s;

-- Select a generic request by ID
SELECT
  request_id, requester_id, authorizer_id,
  request_type, request_status, created_at
FROM
  "GenericRequests"
WHERE
  request_id = %s;

--|----------------------------------------------------------------------------|

-- RequestDescriptions TABLE

-- Insert a new request description
INSERT
  INTO "RequestDescriptions"
    (request_id, requestion_description)
  VALUES
    (%s, %s)
  RETURNING
    created_at;

-- Select a request description by request_id
SELECT
  requestion_description, created_at
  FROM "RequestDescriptions"
  WHERE request_id = %s;

-- Update a request description
UPDATE
  "RequestDescriptions"
SET
  requestion_description = %s
WHERE
  request_id = %s;

--|----------------------------------------------------------------------------|

-- AuthorizedRequests TABLE (for checking authorization)

-- Check if a request type is authorized for a user type
SELECT 1
FROM
  "AuthorizedRequests"
WHERE
  request_type = %s AND
  user_type = %s;

--|----------------------------------------------------------------------------|

-- LOCKOUTS TABLE

-- Insert a new lockout
INSERT
INTO lockouts
  (user_id, reason, expires_at)
VALUES
  (%s, %s, %s)
RETURNING id,
  created_at;

-- Select an active lockout for a user
SELECT
  id, reason,
  expires_at,
  created_at
FROM
  lockouts
WHERE
  user_id = %s AND
  expires_at > NOW();

-- Remove a lockout
DELETE
FROM
  lockouts
WHERE
  id = %s;

--|----------------------------------------------------------------------------|

-- UPGRADE REQUESTS TABLE

-- Insert a new upgrade request
INSERT
  INTO upgrade_requests
    (user_id, notes)
  VALUES
    (%s, %s)
  RETURNING
    id, request_status, created_at;

-- Select upgrade requests for a user
SELECT
  id, request_status,
  notes, created_at
FROM
  upgrade_requests
WHERE
  user_id = %s
ORDER BY
  created_at DESC;

-- Update the status of an upgrade request
UPDATE
    upgrade_requests
  SET
    request_status = %s
  WHERE
    id = %s;

--|----------------------------------------------------------------------------|

-- INVITATIONS TABLE

-- Insert a new invitation
INSERT
INTO invitations
  (document_id, inviter_id, invitee_id)
VALUES
  (%s, %s, %s)
RETURNING
  id, invitation_status, created_at;

-- Select invitations for a specific document
SELECT
  id, inviter_id,
  invitee_id,
  invitation_status,
  created_at
FROM
  invitations
WHERE
  document_id = %s
ORDER BY
  created_at DESC;

-- Select pending invitations for a specific user
SELECT
  id, document_id,
  inviter_id, created_at
FROM
  invitations
WHERE
  invitee_id = %s AND
  invitation_status = 'PENDING';

-- Update the status of an invitation
UPDATE
  invitations
SET
  invitation_status = %s
WHERE
  id = %s;

--|----------------------------------------------------------------------------|

-- BLACKLIST TABLE

-- Insert a new word into the blacklist
INSERT
INTO blacklist
  (word)
VALUES
  (%s)
ON
  CONFLICT (word)
DO
  NOTHING; -- Avoid duplicates

-- Check if a word is in the blacklist
SELECT 1
FROM
  blacklist
WHERE
  word = %s;

--|----------------------------------------------------------------------------|

-- BLACKLIST SUBMISSIONS TABLE

-- Insert a new blacklist submission
INSERT
INTO blacklist_submissions
  (user_id, word)
VALUES
  (%s, %s)
RETURNING
  id, submission_status, created_at;

-- Select pending blacklist submissions
SELECT
  id, user_id,
  word, created_at
FROM
  blacklist_submissions
WHERE
  submission_status = 'PENDING'
ORDER BY
  created_at DESC;

-- Update the status of a blacklist submission
UPDATE
  blacklist_submissions
SET
  submission_status = %s
WHERE
  id = %s;

--|----------------------------------------------------------------------------|

-- LLM REJECTIONS TABLE

-- Insert a new LLM rejection
INSERT
INTO llm_rejections
  (user_id, document_id, reason)
VALUES
  (%s, %s, %s)
RETURNING
  id, llm_rejection_status, created_at;

-- Select LLM rejections for a specific document
SELECT
  id, user_id, reason,
  llm_rejection_status,
  created_at
FROM
  llm_rejections
WHERE
  document_id = %s
ORDER BY
  created_at DESC;

-- Update the status of an LLM rejection
UPDATE
  llm_rejections
SET
  llm_rejection_status = %s
WHERE id = %s;

--|----------------------------------------------------------------------------|

-- ACTIVITY LOGS TABLE

-- Insert a new activity log entry
INSERT
INTO activity_logs
  (user_id, action_type, details)
VALUES
  (%s, %s, %s)
RETURNING
  id, created_at;

-- Select activity logs for a specific user
SELECT
  id, action_type,
  details, created_at
FROM
  activity_logs
WHERE
  user_id = %s
ORDER BY
  created_at DESC;

--|----------------------------------------------------------------------------|

-- USER WHITELIST TABLE

-- Insert a word into a user's whitelist
INSERT
  INTO user_whitelist
    (user_id, word)
  VALUES
  (%s, %s)
  ON CONFLICT
    (user_id, word)
  DO
    NOTHING;

-- Check if a word is in a user's whitelist
SELECT 1
FROM
  user_whitelist
WHERE
  user_id = %s AND
  word = %s;

-- Remove a word from a user's whitelist
DELETE
FROM
  user_whitelist
WHERE
  user_id = %s AND
  word = %s;

--|----------------------------------------------------------------------------|


