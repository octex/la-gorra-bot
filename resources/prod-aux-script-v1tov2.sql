-- WARNING: ONLY FOR PROD OR LOCAL POSTGRESQL DB

ALTER TABLE minions DROP username;
ALTER TABLE minions DROP id;
ALTER TABLE "minions" add primary key (full_username);