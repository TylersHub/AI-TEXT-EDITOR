
-- may help explain the intended structure

--|----------------------------------------------------------------------------|

CREATE TYPE UserType AS ENUM (
  'FREE',
  'PAID',
  'SUPER'
);

CREATE TYPE GenericState AS ENUM (
  'PENDING',
  'ACCEPTED',
  'REJECTED'
);


--|----------------------------------------------------------------------------|


-- StandardRequests are all things with a consistent parameterized query
-- structure, where the only real unknown is whether the request will
-- be accepted or rejected, which also means every request must have
-- an associated responsible party (the authorizer), which means that
-- both the requester and authorizer fields cannot be null


CREATE TYPE StandardActions AS ENUM (
  "SIGN UP ", -- g
  "SIGN IN ", -- f p su g*
  "SIGN OUT ", -- f p su
  "UPGRADE ACCOUNT ", -- f
  "REMOVE ACCOUNT ", -- su
  "PURCHASE TOKENS ", -- f p
  "ADD TOKENS ", -- su sys
  "REMOVE TOKENS ", -- su sys
  "CHECK TOKENS ", -- f p su sys
  "CREATE FILE ", -- f p su
  "CENSOR FILE ", -- sys
  "CORRECT FILE (SELF) ", -- p su
  "CORRECT FILE (LLM) ", -- p su
  "SAVE FILE ", -- p su
  "REMOVE FILE ", -- p su
  "SEND FILE INVITE ", -- p su
  "MANAGE FILE INVITE ", -- p su
  "SEND COLLABORATOR COMPLAINT ", -- p su
  "MANAGE COLLABORATOR COMPLAINT ", -- su
  "MANAGE FILE CORRECTION REJECTION ", -- su
  "ADD WORD ", -- su
  "REMOVE WORD ", -- su
  "CHECK WORDS ", -- su sys
  "LOG WORD FILE ERRORS UPON CREATION ", -- sys
  "LOG WORD CORRECTIONS (SELF)", -- sys
  "LOG WORD CORRECTIONS (LLM) ", -- sys
  "SEE WORD ERROR COUNT ", -- p su
  "SEE WORD CORRECTION COUNT (Self) ", -- p su
  "SEE WORD CORRECTION COUNT (LLM) ", -- p su

);


-- post requests require a document_ID as a parameter

CREATE TYPE StandardActions AS ENUM (
  'USER_LOG_IN', -- users must be logged in to engage
  'USER_LOG_OUT', -- prevents all requests from being processed
  'CREATE_RECORD', -- create file, create document (id set)
  'DESTROY_RECORD', -- removes id set, but leaves posts intact, just orphaned
  'SUBMIT_POST', -- adds user post to Posts with status 'PENDING'
  'DISABLE_POST', -- sets a post's state to 'REJECTED'
  'MUTATE_POST', -- changes the text field of the post (LIMITATIONS)
  'INVITE_COLLABORATOR', -- 'INVITATION'
  'WHITELIST_USER', -- 'WHITELIST'
  'BLACKLIST_WORD', -- BLACKLIST
  'REQUEST_UPGRADE', -- FREE -> PAID
  'UPGRADE_ACCOUNT', -- UPGRADE_ACCOUNT
  'CORRECT_POST', --
  'LLM_REJECTION',
  'FILE_COMPLAINT', -- COMPLAINT
  'LOCKOUT_USER', -- 'LOCKOUT'
  'LOG_ACTIVITY' -- 'LOG'
  'MALFORMED' -- anything not on the request whitelist
)


CREATE TYPE StandardRequestType AS ENUM (
  'POST', -- SUBMIT & DISABLE, MUTATE
  'INVITATION', -- 'INVITATION'
  'WHITELIST', -- 'WHITELIST'
  'BLACKLIST', -- BLACKLIST
  'UPGRADE', -- UPGRADE_ACCOUNT
  'CORRECTION', -- CORRECTION
  'COMPLAINT', -- COMPLAINT
  'LOCKOUT', -- 'LOCKOUT'
  'LOG' -- 'LOG'
  'MALFORMED' -- anything not on the request whitelist
);



--|----------------------------------------------------------------------------|

-- USERS TABLE
CREATE TABLE users (
 id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
 email TEXT UNIQUE NOT NULL,
 password TEXT NOT NULL,
 user_type UserType DEFAULT 'FREE',  -- 'FREE', 'PAID', 'SUPER'
 tokens INT DEFAULT 0
);

--|----------------------------------------------------------------------------|

CREATE TABLE UserPosts (
    PostId INT IDENTITY(1,1) NOT NULL,
    UserId INT NOT NULL,           -- Foreign key linking to the User table
    DocumentId INT NOT NULL,       -- Foreign key linking to the Document table
    CreationDate DATETIME NOT NULL DEFAULT GETDATE(),
    State GenericState NOT NULL DEFAULT 'PENDING', -- Enum: PENDING, ACCEPTED, REJECTED
    Payload TEXT NOT NULL,         -- The actual content of the post
    RelativeOrdering -- What are some options for implementing a this trait?

    CONSTRAINT [PK_Post_PostId] PRIMARY KEY CLUSTERED ([PostId] ASC),
    CONSTRAINT [FK_Post_User] FOREIGN KEY ([UserId]) REFERENCES [User]([Id]),
    CONSTRAINT [FK_Post_Document] FOREIGN KEY ([DocumentId]) REFERENCES [Document]([Id])
);
GO

    -- PostId: A standard auto-incrementing primary key for each post.
    -- UserId and DocumentId: Foreign keys to link each post to the user who
    -- created it and the document it belongs to. This establishes the relationships.
    -- Payload: Using TEXT to store the post content.
    -- State: An enumeration-like field to track the status of the post
    -- (PENDING, ACCEPTED, REJECTED).

--|----------------------------------------------------------------------------|

-- DOCUMENTS TABLE
CREATE TABLE Documents (
 id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
FOREIGN KEY (OwnedBy) REFERENCES Users(UserID),
FOREIGN KEY (LastModifiedBy) REFERENCES Users(UserID)
 created_at TIMESTAMP DEFAULT now(),
 updated_at TIMESTAMP DEFAULT now()

);


-- Document View:
-- [ordered by creation date, filtered by state]
-- this should group by document ID
-- to get a document, query the posts table


CREATE VIEW DocumentView AS
SELECT
    p.PostId,
    p.UserId,
    p.CreationDate,
    p.Payload
FROM
    UserPosts p
JOIN
    [dbo].[User] u ON p.UserId = u.Id
WHERE
    p.State = 'ACCEPTED' -- (optional) OR p.State = 'PENDING'
ORDER BY
    p.CreationDate ASC;
GO

-- -> ^(explanation comment)
-- To get the posts for a specific document,
-- you would then query this view with a WHERE clause on DocumentId.



CREATE TABLE [dbo].[DocumentAuthorization] (
    [DocumentId] INT NOT NULL,
    [UserId] INT NOT NULL,
    CONSTRAINT [PK_DocumentAuthorization]
      PRIMARY KEY CLUSTERED ([DocumentId] ASC, [UserId] ASC), -- Composite primary key
    CONSTRAINT [FK_DocumentAuthorization_Document]
      FOREIGN KEY ([DocumentId]) REFERENCES [Document]([Id]),
    CONSTRAINT [FK_DocumentAuthorization_User]
      FOREIGN KEY ([UserId]) REFERENCES [User]([Id])
);
GO

--|----------------------------------------------------------------------------|


-- collaborators are descibed per document ID
-- they are merely just thos authorized to modify a particular document
-- and by modify we mean submit to
-- there is no deleting posts, just setting to 'REJECTED' which prevents
-- from showing up in the document view

-- to get the collaborator for a particular document,
-- query the DocumentAuthorization table for all UserID
-- where DocumentID is the desired document


-- FUNCTION: GET SHARED DOCUMENTS FOR A COLLABORATOR
CREATE FUNCTION get_collaborator_docs(user_id UUID)
RETURNS SETOF documents AS $$
 SELECT d.* FROM documents d
 JOIN collaborators c ON d.id = c.document_id
 WHERE c.user_id = user_id;
$$ LANGUAGE sql;


--|----------------------------------------------------------------------------|

-- USERS TABLE
CREATE TABLE users (
 id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
 email TEXT UNIQUE NOT NULL,
 password TEXT NOT NULL,
 user_type TEXT DEFAULT 'free',  -- 'free', 'paid', 'super'
 tokens INT DEFAULT 0
);

--|----------------------------------------------------------------------------|

-- DOCUMENTS TABLE
CREATE TABLE documents (
 id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
 owner_id UUID REFERENCES users(id) ,
 title TEXT NOT NULL,
 content TEXT DEFAULT '',
 created_at TIMESTAMP DEFAULT now(),
 updated_at TIMESTAMP DEFAULT now()
);

--|----------------------------------------------------------------------------|



--[SPACER]



--|----------------------------------------------------------------------------|



-- this should be just like the Authorization Table;
-- reference to the original (rejected) post (since never delete)
-- reference to the proposed replacement

-- CORRECTIONS TABLE
CREATE TABLE corrections (
 id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
 document_id UUID REFERENCES documents(id) ,
 user_id UUID REFERENCES users(id) ,
 type TEXT CHECK (type IN ('llm', 'manual')),
 original_text TEXT,
 corrected_text TEXT,
 status GenericState DEFAULT 'PENDING',
 tokens_used INT,
 created_at TIMESTAMP DEFAULT now()
);



--|----------------------------------------------------------------------------|

-- COMPLAINTS TABLE
CREATE TABLE complaints (
 id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
 complainant_id UUID REFERENCES users(id) ,
 accused_id UUID REFERENCES users(id) ,
 document_id UUID REFERENCES documents(id),
 reason TEXT,
 status GenericState DEFAULT 'PENDING',
 created_at TIMESTAMP DEFAULT now()
);

--|----------------------------------------------------------------------------|



--|----------------------------------------------------------------------------|





CREATE TABLE GenericRequests (

status GenericState
  request_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  requester_id UUID REFERENCES users(id) NOT NULL,
  authorizer_id UUID REFERENCES users(id) NOT NULL,
  request_type RequestType
    NOT NULL DEFAULT 'MALFORMED' , -- unsure NOT NULL?
  request_status GenericState
    CHECK (status IN ('PENDING', 'ACCEPTED', 'REJECTED'))
    DEFAULT 'PENDING',
  created_at TIMESTAMP DEFAULT now()
)

-- this is for the purpose of query parameterization, to seperate
-- the user data from the rest of the query (which goes ahead of it)
CREATE TABLE RequestDescriptions (
  request_id UUID PRIMARY FOREIGN KEY DEFAULT uuid_generate_v4(),
  requestion_description TEXT DEFAULT ""
  created_at TIMESTAMP DEFAULT now()
)

--|----------------------------------------------------------------------------|



CREATE TABLE AuthorizedRequests (
    request_type StandardRequestType NOT NULL,
    user_type UserType NOT NULL,
    PRIMARY KEY (request_type, user_type)
    -- You can optionally add foreign key constraints if your database system supports
    -- referencing ENUM types directly in foreign keys. However, support can vary.
    -- If not directly supported, you might manage these constraints at the application level
    -- or by creating separate lookup tables (though that might be overkill for simple ENUMs).
);
GO



--example of querying
SELECT COUNT(*)
FROM AuthorizedRequests
WHERE request_type = 'WHITELIST' AND user_type = 'PAID';

-- If the count is greater than 0, they are authorized.


SELECT 1
FROM AuthorizedRequests
WHERE request_type = 'WHITELIST' AND user_type = 'PAID';

-- If a row is returned, they are authorized.

--|----------------------------------------------------------------------------|

INSERT INTO AuthorizedActions (action_type, user_type) VALUES (USER_LOG_IN , FREE   )
INSERT INTO AuthorizedActions (action_type, user_type) VALUES (USER_LOG_IN , PAID   )
INSERT INTO AuthorizedActions (action_type, user_type) VALUES (USER_LOG_IN , SUPER  )

INSERT INTO AuthorizedActions (action_type, user_type) VALUES (USER_LOG_OUT , FREE  )
INSERT INTO AuthorizedActions (action_type, user_type) VALUES (USER_LOG_OUT, PAID   )
INSERT INTO AuthorizedActions (action_type, user_type) VALUES (USER_LOG_OUT , SUPER )


INSERT INTO AuthorizedActions (action_type, user_type) VALUES ( CREATE_RECORD , PAID  )
INSERT INTO AuthorizedActions (action_type, user_type) VALUES ( CREATE_RECORD , SUPER )

INSERT INTO AuthorizedActions (action_type, user_type) VALUES ( DESTROY_RECORD , PAID  )
INSERT INTO AuthorizedActions (action_type, user_type) VALUES ( DESTROY_RECORD , SUPER )

INSERT INTO AuthorizedActions (action_type, user_type) VALUES (SUBMIT_POST , FREE )
INSERT INTO AuthorizedActions (action_type, user_type) VALUES (SUBMIT_POST , PAID )
INSERT INTO AuthorizedActions (action_type, user_type) VALUES (SUBMIT_POST, SUPER )

INSERT INTO AuthorizedActions (action_type, user_type) VALUES (DISABLE_POST , PAID )
INSERT INTO AuthorizedActions (action_type, user_type) VALUES (DISABLE_POST, SUPER )


INSERT INTO AuthorizedActions (action_type, user_type) VALUES (REQUEST_UPGRADE, FREE )
INSERT INTO AuthorizedActions (action_type, user_type) VALUES (UPGRADE_ACCOUNT, SUPER )






--|----------------------------------------------------------------------------|

-



