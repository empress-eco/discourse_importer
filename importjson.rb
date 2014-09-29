require File.expand_path(File.dirname(__FILE__) + "/base.rb")

require "time"

class ImportScripts::ImportJSON < ImportScripts::Base

  def execute
    import_users
    import_posts
  end

  def import_users
    puts '', "creating users"
    userjson = "/shared/importdata/users.json"

    results = JSON.parse(File.read(userjson))

    create_users(results) do |user|
      { id: user['id'],
        email: user['email'],
        username: user['username'],
        created_at: Time.parse(user['created_at']),
        moderator: false,
        admin: false}
    end
  end

  def import_posts
    puts "", "creating topics and posts"
    messagesjson = "/shared/importdata/messages.json"

    results = JSON.parse(File.read(messagesjson))

    create_posts(results) do |m|
      skip = false
      mapped = {}

      mapped[:id] = m['post_id']
      mapped[:user_id] = user_id_from_imported_user_id(m['user_id']) || -1
      mapped[:raw] = m['message']
      mapped[:created_at] = Time.parse(m['created_at'])


      if m['post_id'] == m['first_post_id']
        mapped[:category] = category_from_imported_category_id(m['category']).try(:name)
        mapped[:title] = CGI.unescapeHTML(m['topic'])
      else
        parent = topic_lookup_from_imported_post_id(m['first_post_id'])
        if parent
          mapped[:topic_id] = parent[:topic_id]
        else
          puts "Parent post #{m['first_post_id']} doesn't exist. Skipping #{m["post_id"]}: #{m["topic"]}"
          skip = true
        end
      end

      skip ? nil : mapped
    end
  end

end

ImportScripts::ImportJSON.new.perform
