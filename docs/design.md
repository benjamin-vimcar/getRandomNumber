# Spec

We must create a RESTful API. It must be written in Python, and should use Flask. It must have the following features:

* Sign up
    - Create an account with an e-mail and password
    - Send a confirmation e-mail
    - A user must click the link in the e-mail to activate their account
* Authentication
    - A user can login with their chosen e-mail and password
* Authorisation
    - A user can access a protected resource only if authenticated
    - Anonymous access is not possible.

See https://github.com/vimcar/backend-challenge#voluntary-additions for the set of additional desirable features.

# Approach

I spend an hour thinking about design yesterday, and have this afternoon to actually create something. In the interests of getting an MVP out, I'll therefore be leaning heavily on technologies I'm already familiar with.

My overall plan is to produce a spec for the user experience, use this to design and implement the classes/structures/etc in the underlying code. Initially, I will mock out the HTTPS server, datastore, and authentication layer. This should make initial testing much simpler.

# User experience

First, let's document a user experience that would meet the spec. I'm going to use [OpenAPI v2](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md) - it's a mature system for describing HTTP(S) APIs with good tooling and with which I am very familiar.

See api.yaml.

# The actual back-end

Now that we've written an API and generated a server framework from it, we now need to create the logic to actually implement the spec. We'll put this in its own module, which the server will later import. This will allow us to write UTs in the 
