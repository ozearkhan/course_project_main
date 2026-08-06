=============================================
File: LCA-LangSmith-C1-M0-V3-Setup-Guide.txt
=============================================

[00:00:00] 



nick: Welcome to the introduction to LangSmith course. In this video, we're going to walk you through how to set up your LangSmith account. We're going to generate an API key in LangSmith, and then we're going to hook that API key up to an application that we're going to be using throughout this course. To get started, go ahead and navigate over to the smith.langchain.com website.

Here, you can sign up for an account in a few different ways, including with a Google, GitHub or Discord account, or just with your email. Once you sign up for an account, go ahead and go through the brief onboarding flow, and then you'll end up in an interface that looks something like this. 

The first thing that we'll want to do here is actually navigate over to [00:01:00] the settings pane.

We'll go ahead and find the API Keys tab. Here, using this button, , We're going to create our API key that we can use to hook up to our application. A personal access token is fine. Go ahead and give it a description and store it somewhere safe as we'll be using it throughout this course.

Once you've created your API Key for LangSmith, you'll also need to create an API key for OpenAI as OpenAI is the model provider that we use throughout this course. If you haven't done so yet, go ahead and pause the video and follow some of the setup instructions to create your OpenAI API Key.

Cool. Now that we have an OpenAI API key and a LangSmith API key, let's go ahead and add those keys to our application. In the description for this video and for this course, there is an associated GitHub repo with a series of notebooks that we'll [00:02:00] work through. Go ahead and open the notebook for Module zero called RAG Application.

Just like the name suggests, we're going to be using a RAG application throughout this course. For those of you who aren't familiar with RAG, RAG is a very popular approach right now for augmenting pre-trained LLMs with documents that have information specific to your use case.

A RAG flow is quite simple. We're going to take in a user's question. With that question, we're going to query a vector database, which is similar to search, and find documents that are relevant to that question. Once we retrieve these documents, we're going to go ahead and provide both the documents and the original question to an LLM, in our case an OpenAI model. This model is then going to generate an answer, which we're going to return to the user.

To get started, [00:03:00] let's go ahead and set up our environment variables. Go ahead and set the OpenAI API key and LangChain API key that we just generated in LangSmith. We're also going to need to set LangChain tracing V2 equal to true to enable tracing from our application to LangSmith. You'll also need to set a project name.

And in our case, that's going to be langsmith-academy. We're going to be using these environment variables a lot, and so it might be useful if you actually set them in a .env file, which is what I've done.

Now let's walk through our RAG application. We're going to just actually start from the function at the bottom here, and the implementation matches exactly what we saw in the diagram above. Our top level function is called langsmith_rag. This takes in a question input from the user and it calls retrieve_documents, passing in that question.

Retrieve_documents, retrieves documents [00:04:00] that are relevant to the question. And let's go ahead and take a look at the function definition here. You can see that we invoke a retriever. This retriever actually has documents about LangSmith itself, and so this is going to be pretty fun. We're going to be asking this application questions about LangSmith and then using LangSmith to take a look at what's happening in our application.

Once we return these documents, we then call generate_response with both the question and the documents retrieved. This generate_response function will take in the question and documents. It will format the documents into a single string, and then it will call this function called call_openai. This makes a chat completion to OpenAI with our passed in messages, and we finally will return the response all the way through and we'll return the first choice in the message and the content to the user.

[00:05:00] Let's go ahead and run our application here. The first time that you set up this model it might take a second because we're going to be indexing and storing LangSmith documentation. Let's go ahead and ask it a simple question. What is LangSmith used for? We'll pass this into the langsmith_rag function and we'll see that it executes and returns.

LangSmith is a platform designed for development, monitoring and testing of LLM apps, which is pretty good. Now let's go back to LangSmith and take a look at that project. If we navigate back to our home page in LangSmith, we'll see that we now have a project with the same projects name that we set in the repo.

If we click into langsmith-academy, we can see the trace that was just sent from us executing this application. In the next module, we're going to go deeper into how to set up tracing in your application, and we'll also take a closer look at this UI and break down what the different components of a trace are.[00:06:00] 

See you there.



=============================================
File: LCA-LangSmith-C1-M1-L1-V3-Tracing-Basics.txt
=============================================

nick: [00:00:00] In this video, we're going to walk through how to set up observability in your LLM application. We'll start by introducing some high level tracing concepts that we use in LangSmith. Then we'll dive into the code of our RAG application and set up tracing using the LangSmith package. From there, we'll take a look at the LangSmith UI and see exactly what types of information we can send in traces.

At the highest level, we have a project. A project is pretty one-to-one with any application that you're working on. In our case, our project is our RAG application. In a project, we have a collection of traces. You can think of each trace as an invocation of your application. This means that anytime a user runs our application, we're going to publish a new trace to LangSmith.

If a trace is an end-to-end execution of your application, then each unit of work or logic within your trace [00:01:00] is a run. In our RAG application, we have two main runs. We have the retrieve documents function and the generate response function. It's important to note that runs are a nested and recursive concept. For any trace at the top level, we have a root run that's one-to-one with the trace. Beneath that root run, we have our retrieve documents and generate response runs.

It's important to see that even these runs have their own nested sub runs that have even more specific information for a particular piece of logic.

Each of these runs contains several run attributes, and this is where all of the useful information for a run lives. As an example, let's take a look at a retrieve documents run. For each run, we'll get to see the input and the output. For our retrieve documents run, the input is going to be the user's question, and the output is going to be the relevant [00:02:00] documents that we've retrieved.

We can also pass custom metadata to a run. This might be something like the database provider or the version of your application that published this run. We'll see this a little bit later, but metadata is really useful in LangSmith because you can filter on specific keys and values to focus on a particular group of runs that you care about.

Later on in this module, we'll also talk a bit more about run types. There's also a lot of useful telemetry that can be tied to a run. This can include the latency, the token count, and also custom feedback that's provided. In our case, a piece of feedback might be provided by the user on whether or not the retrieved document is actually good.

Let's go ahead and navigate over to our tracing basics notebook. You can find this in module one of the GitHub repo for this course. In this notebook, we're going to take a look at the same RAG [00:03:00] application that we showed in the setup video, and we're going to show how you can set up tracing with the traceable decorator.

The first thing that you need to do here is to set your environment variables. These are the same variables that we set in the Setup notebook. You can set them in line or use a .env file to load them in.

Let's do a quick review of our existing RAG application. If you want more specifics, you can rewatch the setup video where we dive into what each function does. At a high level, we have a top level LangSmith RAG function, which kicks off our RAG flow. This calls retrieve_documents, which will fetch some documents from a vector database.

These documents are then provided to our generate_response function, which will actually call OpenAI and [00:04:00] generate our chat completion. This chat completion is then finally returned to the user. In order to set up tracing, we'll use the traceable decorator. The traceable decorator is, in my opinion, one of the easiest ways to set up tracing in your application.

The first thing that we need to do is import this decorator from the LangSmith package.

In order to set up tracing, all we need to do is add the traceable decorator to each of our functions. Let's go ahead and do that.

What Traceable enables under the hood is whenever we run a function with the decorator, we create a run tree when the function is called. We also detect if this is a root run. In other words, a new [00:05:00] trace, or if there's already a parent run, and this new run is actually a nested function call. If we see that the function that is being called is decorated with traceable, and that the parent function is also decorated with traceable, we'll actually insert this new run into the parent run tree, and this is how we build our run tree to mimic the shape of our nested function calls.

By default, decorating a function as traceable means that we'll stream the name of the function and also the inputs. When the function returns or if it throws an error, we'll patch the output as an update to the trace. It's important to note that all of this happens on a background thread, so there's no latency actually added to your application.

Now that we've added traceable to every function in our RAG application, let's go ahead and run it.

Cool. Let's take a [00:06:00] look in LangSmith. If we navigate to the tracing projects pane in LangSmith, we'll be able to see a new tracing project called langsmith-academy. When we click into this project, we'll be able to see all of the traces within langsmith-academy. Let's click into our latest trace. Here we get a closeup view of our run tree.

We can see that the run tree clearly outlines each step within our application. For each run, including the root level run, we can see the inputs and the outputs.

At the root level, this means we see the input question that's passed to the user and the output that finally comes out of the LLM. Notice that this has been rendered quite nicely. If we want to see the raw output, we can also see the payload that we actually passed to LangSmith. Let's go ahead and click into the retrieve documents run so [00:07:00] that we can see the input and output of this particular step.

We can see that we've retrieved four documents that are hopefully helpful to answering your user's question. Later on, in the generate response run, we can see that we pass in the user's question along with those four documents as input. Then finally, we call OpenAI and return the response to the user.

Right now our run tree is still pretty small, but with more complex applications, you can imagine how this run tree can grow pretty big pretty quickly. I can quickly collapse my [00:08:00] run tree to just look at the top level runs. I can also optionally look at different stats, including the latency. In this case, we can see that we're almost entirely bottlenecked on the generate response step . We can see a waterfall visualization of this timing.

nick: This is really helpful to know when we iterate on our application's architecture so that we can try and slim down or parallelize expensive parts of our application. I also mentioned earlier that filtering is built into LangSmith in several places. One place where we can filter is within a trace. A really common flow is to filter over a particular metadata value.

Let's take a look at what metadata we get by default on our runs. We can see that we were able to trace with the traceable decorator. We can also see that we have some information about our runtime, including the version of the LangSmith SDK that we're using, and the Python version. This can be really useful when we're trying to debug any weird version conflict [00:09:00] errors.

Now, let's go ahead and add some custom metadata to our application so that we can send some more information up with this trace. Metadata is just a dictionary of key-value pairs that can be attached to runs. Common use cases for metadata include passing up the model provider and the model that was used, as well as the version of the application that generated the run.

Let's go ahead and add some metadata to our existing application. For the retrieve documents function, some useful metadata might be the name of the vector database that we're using. Let's go ahead and pass a key called vectordb and make the value sklearn.

Now for our call OpenAI function, let's pass the model name and the model provider that we're using.[00:10:00] 

Cool. Let's go ahead and run this again.

We can see that our application actually does a pretty good job answering this time, which is pretty fun. Let's go ahead and see how this looks in LangSmith.

If I click into this latest trace, I can now see when I click on retrieve documents that we have this new vectordb key with the sklearn value. I can also see in call_openai, that we have the model_name and the model_provider. Now let's [00:11:00] filter down to runs where this model_provider key always has the value of openai.

As we can see, this will filter down to just this call_openai run. So far we've only been passing metadata in statically in the traceable decorators. It's also worth noting that you can pass metadata in at runtime. When we call a function decorated with traceable, we can pass in a second field langsmith_extra that takes in a dictionary where one of the keys is metadata.

nick: Here you can pass runtime metadata of your choice. Let's go ahead and run this and take a look at what it looks like in [00:12:00] LangSmith. Navigating back to LangSmith. If I click on this latest trace, I can see that we have this new piece of metadata that we passed at runtime.

Finally, I just want to note that it's really easy to share runs with your colleagues. This can be really helpful when one of your colleagues might have more experience with a certain part of the application.

nick: If I'm getting confused by some behavior, I can just click on this share button, which will give me a link to share with one of my colleagues with more expertise and they'll be able to look directly at this run.

To recap in this video, we learned about projects, traces, and runs, as well as how to set up tracing for a Python LLM application. We also added custom metadata to our runs, both statically and at runtime. Thanks for following along.



=============================================
File: LCA-LangSmith-C1-M1-L2-V3-Run-Types.txt
=============================================

nick: [00:00:00] In this video, we're going to walk through the different types of runs that you can create when tracing in LangSmith. When building LLM applications, it's really important to have a good sense of what's happening under the hood. The first step in achieving this observability is logging, and logging is a great start, but we've all experienced what it's like to try and parse through a huge unformatted stack trace just to find the root cause of an error.

This can be particularly hard for LLM applications because there can be a lot of text to read through. We spent a lot of time working on the UX for traces in LangSmith so that different components of your application will get rendered in specific ways. Let's dive into how we can use the traceable decorator to create these different types of runs and the usability features that come with each type.

We have several different types of runs in LangSmith. Let's walk through them. LLM runs involve invoking an LLM or chat model. [00:01:00] Retriever runs involve fetching supplemental documents or data from some external source. The Tool run is used whenever we use a model that creates a tool call as an output. Chain is our default type of run, which just signifies an arbitrary step of execution in our application.

Most runs that have nested children are Chains and are used to group several sub-runs into a single larger process. Prompt runs typically involve creating a prompt from a template, and Parser runs are used to parse some unstructured output into a structured schema. Let's navigate over to our Run Types notebook.

In this notebook, we're going to be walking through a few of these different types of runs that we just mentioned. We'll see how we can pass information to LangSmith so that these runs are processed , rendered, and some associated features for each run type. . First, let's go ahead and add our environment variables just like we've been doing either in line or pulling from a [00:02:00] .env file.

The first type of run that we're going to talk about is the LLM run type. In this code, we've mocked out the inputs and the outputs for a chat model. If we have a decorated traceable function with a run type of LLM where the inputs and outputs follow these specific formats, then LangSmith will be able to render the input and output messages nicely in the UI.

Let's take a closer look at our required formats. We're taking in input messages in the list, and each input message needs to have a role which specifies the sender of the message along with an actual content string. We have a few options for formatting the return output from the function. We can wrap a full output object, which includes this choices key.

We can also get rid of the choices key and just return the message itself. It's also acceptable to get rid of this message wrapper and [00:03:00] just return a dictionary with a role and the content. And it's also okay just to return a list with two items where the first item is the role, and the second item is the content.

Here we have a dummy chat model invocation that we've decorated with traceable. Let's go ahead and run it twice. First, we'll run it without specifying any run type. This means that the run type will default to Chain. Now let's specify a run type of LLM.

Let's pivot over to LangSmith and compare these traces side by side. Let's go ahead and click into our most recent trace. This is the trace that was sent with a run type of LLM, and we can immediately see that reflected with this icon here. Now let's find, and click the compare option, and select the second most recent trace that we just sent.

This opens up a [00:04:00] comparison view where we can look at our most recent trace and the one we sent right before side by side. We can see different icons for the different run types. ~. When we set the run type equal to LLM, we get this nicely rendered AI message output when our default run type is still a Chain, our rendered output still looks like raw JSON.~

This is mostly a cosmetic nicety, but there's a more important part to specifying a run type of an LLM. If I close out the comparison and return to our most recent trace with an LLM run type, we can see that there's a button here that will allow us to open to the playground. Let's go ahead and click it.

This takes us directly to LangSmith's playground interface. We'll cover the playground in much more depth in the later module, but as a sneak peek, the playground is a sandbox iteration environment within LangSmith where you can quickly iterate and test out new prompts. By specifying your run type as LLM, you can immediately jump from a trace into this playground and have it preload with all of the existing messages from your run.

Note that we didn't use a real model in our function this time, so we just defaulted to GPT-5.4, or whichever option found at the top of [00:05:00] this list. . Let's head back over to our tracing project. If we click into our second to last trace, where the default run type is still Chain, we can see that the playground button is not available, and we can't access the playground even though our response format was the exact same.

Now let's go ahead and make one more change to our traceable decorator. We're going to add metadata with two specific fields, ls_provider and ls_model_name. Providing these two fields makes it possible for LangSmith to identify which model you're using and attribute tokens and cost to this run.

Let's take a look.

Let's take a look at our new trace.[00:06:00] 

We can see that these metadata values were correctly pushed up. We can also now jump directly into the playground and see that our chosen model is defaults populated for us to test with.

Our next topic is how to handle tracing for streaming LLM applications. For a lot of LLM applications, our outputs will come back in a streaming manner, and this is something that we need to handle when tracing so that we can still make use of those rendering niceties that we get with the LLM Run type.

Here, we've mocked out a function called my_streaming_chat_model. This will effectively just yield us a short string, but as a list of objects, which mimics how streaming outputs often come back in individual chunks. Let's go ahead and run this once as is.

You can see at the top of the snippet, we have a function called reduce_chunks. What this effectively does is it takes that list of chunks passed back from the stream and then formats them into one of the valid output [00:07:00] formats for LLM run types that we just saw above. Let's go ahead and add this reducer function as an argument in the traceable decorator.

Now let's run it again and compare these two streaming.

Clicking into the most recent trace and comparing it again with our second most recent trace. We can see the difference in rendering~ right away.~ This reducer allows us , to render a slightly more tidy AI message, even though our output came back in a streaming format.

Now let's take a closer look at retrieval. A lot of LLM applications require looking up documents from vector databases, and retrievers are the mechanisms through which we can retrieve these documents.

Because documents are so important and fundamental, LangSmith renders these documents in a special format so that they're easier to view. [00:08:00] In order to do this, we need to pass in documents according to a particular specification, just like we did for the inputs and the outputs of LLM runs. First, let's go ahead and add a run type of retriever so that we can easily distinguish this run from others based on its icon.

~Let's go ahead and run this code as is. ~Here, we're returning a dictionary with three keys, page_content, doc_type and metadata. ~And this is wrong on purpose. ~The key should actually be type instead of doc_type. Let's go ahead and correct this and make that key type, and run it.

Taking a look now in LangSmith , at my last trace, , I can see documents that can be viewed one at a time. This can be ~really ~helpful when debugging RAG applications. ~As this UI is much easier to read than the raw JSON. ~ ~You can also click into the documents to see their content in more detail as well as the metadata.~

The final type of run that I want to show today is the Tool run. Some model providers provide a function or tool calling interface, including OpenAI. What we have here is a mocked out function called ask_about_the_weather. [00:09:00] Ask_about_the_weather has access to a tool called get_current_temperature.  Ask_about_the_weather invokes call_openai with this tool bound to the model, which gives the LLM the discretion of whether or not to invoke this tool.

Here, our tool just returns a pseudo response back to our chat model and then asks it to generate the final output. Let's go ahead and decorate this tool function with the Tool run type.

Now let's go ahead and ask about the weather in New York City by passing in these input messages.

In LangSmith, we can see that our first LLM call recognizes that we have access to a tool called get_current_temperature. This tool is then actually invoked. And then finally, we can see this tool message in the chat message history that provides the tool call's output, which helps generate our final response from the [00:10:00] LLM.

To recap, we just covered how to trace various different types of runs, how they're rendered, and some associated features. Thanks for watching.



=============================================
File: LCA-LangSmith-C1-M1-L3-V3.1-Alternative-Traces.txt
=============================================

nick: [00:00:00] So far in this course, we've been using the traceable decorator to add tracing to our application and log these traces to LangSmith. In this video, I want to talk about a few alternative ways to set up tracing in your application and discuss when we might want to use these different techniques. Let's navigate over to our alternative tracing methods notebook.

Like we've seen so far, the traceable decorator is the default way to set up tracing. There are some advantages to this. For one, you don't need to make a lot of changes to your code. You just need to add a decorator to the functions that you want to trace. The decorator will by default manage the run tree for you, and it will detect when you make nested function calls so that you can automatically build your run tree.

We also automatically trace the inputs and the outputs of each function in your run tree. Tracing with the traceable decorator is really easy to set up, but there are cases where it might be even easier to set up tracing and also cases where you might want some more [00:01:00] granular and detailed control over what you trace.

So let's talk about a few of these other approaches.

The first approach I want to talk about is if you're actually using LangChain or LangGraph, our open source packages to build your application. When you're using LangChain or LangGraph, all of the LangChain components that you're using and all of the nodes that you've defined in LangGraph will automatically get traced to LangSmith.

All you need to do is set these environment variables that we've already been setting. Specifically, you need to set your LANGCHAIN_API_KEY, and you need to set LANGCHAIN_TRACING_V2 equal to true.

In this next cell, I've defined that same RAG application that we've been using so far, only with LangGraph primitives instead of with raw Python code. I wouldn't worry too much about the actual implementation here. LangGraph is really powerful, and if you're interested in learning more, we have a LangChain Academy [00:02:00] module for an Introduction to LangGraph.

It's worth noting as well that the different nodes in our graph make use of LangChain components, and so both the nodes which are a part of LangGraph and the components which we leverage from LangChain's libraries will be traced automatically. Let's go ahead and create our graph. We can see that we've built a very simple RAG pipeline here.

I also want to note that you can pass metadata into LangGraph executions as well by specifying it in an additional config argument that invoke takes. Let's do that here. You can see, and we pass metadata where the key is foo and the value is bar. Now let's go ahead and run this graph.

Cool. Let's take a look in LangSmith. Looking into our trace, we can see a run tree that looks very similar to what we've seen so far with traceable for our RAG application. We can also see that we have the metadata passed up [00:03:00] that we just included. This was a LangGraph invocation, and we can see that we have our two nodes retrieve_documents and generate_response.

And then within them we have our call to our VectorStoreRetriever, and we also have our call to ChatOpenAI. Once again, note that we didn't add traceable anywhere in this application and we didn't trace in any other way. This was all done by default, just by setting our environment variables and leveraging LangChain and LangGraph.

Cool. So that was an example of where sometimes you don't even need to use traceable to set up tracing in your application. This next scenario is kind of on the other side where you actually need more granular control than what traceable offers. The tracing context manager is something that you can use in Python.

This is really useful when you might want to log a trace for a specific block of code that is maybe [00:04:00] not in a function at all, or is maybe just a subset of the logic in a function. Like we mentioned, traceable will by default manage the function calling tree for you and will also automatically log the inputs and the outputs for that function.

But sometimes what you want to log is actually within the function itself. Let's take a look at an example where we can use our context manager to log a specific input and output of our choice. Here we have the same RAG application as before. We're using traceable over each of our functions. Let's go ahead and run this once as is.

Cool. Now for this particular function, generate_response, let's say that we don't actually want to log the documents that come in as a list of objects but we actually want to trace the formatted doc string that's actually passed up to our chat model. First, let's go [00:05:00] ahead and get rid of this traceable decorator here.

We are going to add in a context manager to trace at a more granular level within the function call itself. Let's walk through the arguments of our context manager. First, we create a name for this trace. We also specify a run type, which for us is just chain. We can see that we're taking in both the question and the formatted doc string as inputs instead of the list of documents that came into the function.

These inputs are crucially different than what we would've gotten with traceable. Note that we don't actually specify any outputs here because we don't have them yet. We'll patch our outputs later on. And finally, we can also pass in metadata with this trace context manager, just like we're doing here with this metadata argument.

With this context, we can now indent this logic so that it falls under our tracing context. [00:06:00] We format our messages just like before, and then we call OpenAI. Once we get our response from OpenAI, we can log that response using ls_trace.end. This will end our tracing context and we'll also patch our output to LangSmith so that it shows up in the trace.

Let's go ahead and try running it.

Heading back to LangSmith. Let's look at our two traces side by side.

nick: I can see that in my generate response step, I've now passed the question and the formatted doc string, whereas before we had our list of document objects. We also get the output, which is the chat completion. We [00:07:00] got this completion after the fact, and this was patched to LangSmith, when we called ls_trace.end.

We can see that with our context manager, we were able to have more granular control over exactly which inputs and outputs we logged and when we logged them. And finally taking a look at the metadata, we can see that we've passed up foo bar once again. And we can see our use of trace, or traceable.

Cool. The last method that I want to share with you is called wrap_openai. Wrap_openai is something that we made specifically for our users who already have existing code that calls the OpenAI SDK directly. All of the other methods we've talked about so far would also work. You could use at traceable, in which case you'd have to move that OpenAI call into a particular function that takes those inputs and outputs in a certain way.

We could also migrate to using a LangChain component, and we can also use our context manager around those specific calls to make sure that they're logged in the [00:08:00] correct format. However, we think it's actually a lot easier and a lot more surgical if we just go ahead and wrap the OpenAI client with our wrap_openai wrapper.

This is really helpful because now any calls to OpenAI through your client will automatically get traced to LangSmith. Let's take a look at our code. Previously, we had this separate function called call_openai. This was being traced with traceable. Let's go ahead and run this once as is.

Now, let's import our wrap_openai wrapper from LangSmith wrappers.

We'll also go ahead and wrap our OpenAI client with that wrapper.

Awesome. Let's go ahead and get rid of [00:09:00] this function altogether and just directly call our chat completions endpoint. Keep in mind, we're losing this traceable decorator, which specifies the run type as LLM. .

Cool. Let's go ahead and run this again.

Now when we take a look in LangSmith, we can see that we still have this ChatOpenAI, LLM type run, even though we made our call through the OpenAI SDK without traceable. You can see the inputs and the outputs are all also rendered. ~Nicely, which is another benefit of using wrap_openai~~.~

Finally, I want to note that wrapping the OpenAI client also gives us the ability to pass additional fields in through langsmith_extra, including metadata on our run. Let's [00:10:00] go ahead and run this completion and then take a quick look in LangSmith.

Taking a look at our latest completion, and then moving over to the attributes tab , to see our metadata, we can see that we were able to pass up foo bar once again with LangSmith Extra.

To recap, let's walk through our different tracing methods once again. Traceable is the default way to set up tracing. It manages your run tree, as well as automatically traces the inputs and the outputs for each function for you. With LangChain or LangGraph, you get tracing out of the box for free.

You can also use a tracing context manager when you want more control over exactly what your tracing and which inputs and outputs you're going to log. Wrap_openai also allows you to add tracing to your code very surgically so that if you're already using the OpenAI SDK, or you want to use it directly, all you need to do is wrap the client.[00:11:00] 

There's another technique called Run Tree, which we're not going to cover in this video, but it's an even more controllable and granular interface for tracing. One example of when this is helpful is when you need to get the run ID from your trace so that you can use it in your application in some other way, whether it's to add user feedback through the SDK or to log that run ID to another service.

Thanks for following along.



=============================================
File: LCA-LangSmith-C1-M1-L4-V3-Conversational-Threads.txt
=============================================

nick: [00:00:00] In this video, I want to talk through the concept of conversational threads and why it's particularly relevant for LLM applications. We're also going to step into LangSmith and take a look at how we show conversational threads and how you can use this concept to track full iterations between a user and your application.

For a lot of applications built with LLMs, there's going to be some sort of chat interface. This is something that Gen AI really excels at. Let's take a look at one of our own production applications, Chat LangChain. You can think of Chat LangChain as a Chat GPT like interface where users can ask questions about LangChain, LangGraph and LangSmith.

Like most chat interfaces, there's going to be a back and forth between the user and Chat LangChain, and so users will be able to ask follow-up questions. While each question that the user asks publishes a new trace, these traces have more meaning when viewed together. This is because the chat [00:01:00] history has important context for the follow-up questions that are asked, and so it's often useful to be able to see all of the traces tied to one conversation with the application as opposed to looking at each trace individually.

To that end, we have this concept of conversational threads. You can think of threads as a higher level abstraction where a thread will contain a series of traces where each trace is an invocation of your app. Let's go ahead and take a look at how to set up threads in our own code so that we can log traces to LangSmith tied under a single thread.

First, as always, we're going to import our environment variables and make sure we have tracing set up in LangSmith.

Like we just discussed, each invocation of your app is its own trace, and these traces are linked together in a series by being a part of the same thread. In order to link these traces together, we're making use of the [00:02:00] metadata field in our traces. Specifically, we need to pass one of three keys, session_id, thread_id or conversation_id.

The value is going to be a UUID that will be the unique identifier for your thread. Let's go ahead and create a thread ID using the Python UUID library.

Here we have the same RAG application that we've been using throughout this course. Let's go ahead and define it.

Earlier on in this course, we showed how we can use the langsmith_extra field to dynamically pass metadata to a trace. Here we're going to pass in a single key for thread_id and give it our generated UUID value. We're going to go ahead and ask two questions through our application. This is to mimic an interaction with an application where a user is going to first ask one [00:03:00] question and then ask a follow-up.

Note that for both of these questions, we've passed in the same thread ID in the metadata. Let's go ahead and take a look in LangSmith. We can see that the two most recent traces in our project correspond to those two questions that we just asked. If I click into the most recent trace, I can see that we have a thread button in the upper right hand corner here.

This is because in our metadata, we now have access to this thread_id field. Let's go ahead and click on this thread button. This has navigated me to the thread, turn view, , for this particular trace. Here we can see the full conversation history with all of our associated traces to this thread_id. ~We can see both of the traces here.~

We can also see the total number of tokens that we've used, as well as our average and extreme latency metrics. We also have this collated view of the different traces, and we can see the back and forth between the human and our application with the inputs and the [00:04:00] application outputs.

Toggling to the Trace View, Gives us the ability to step into a single trace, so that we can see exactly what happened in each turn. We essentially have a stacked trace view that allows us to dive into every turn of this interaction. You can also navigate to this threads view without first going through a trace.

Let's go back to our langsmith-academy tracing project. Here, under the Threads tab, We can see that we have a table with all of the threads in our project.

This view can be really useful if you want to debug a full interaction between a user and your application that might have taken up multiple traces. A great way to start is by ~coming to this threads view and~ filtering down to a particular thread.

That's an overview of conversational threads, and that wraps up our first module in LangSmith. See you in module [00:05:00] two.



=============================================
File: LCA-LangSmith-C1-M2-L1-V3-Datasets.txt
=============================================

nick: [00:00:00] In this video, we're going to talk through datasets in LangSmith. Datasets are a core piece of offline evaluations. Offline evaluations are really important to make sure that as you make changes to your application, performance is actually getting better. As you add new prompts, swap between different model providers or even change the architecture of your application, you want to make sure that your application's performance is improving and not regressing, and that these improvements are worth any potential trade-offs with latency or token usage cost.

I've seen a lot of LLM apps go into production from just a quick gut check by testing over a few examples. This isn't sustainable, especially for more sensitive and complex use cases. In order to test and evaluate our application over time, we need to build good evaluation datasets. Datasets are fundamentally just a list of examples.

We can create this list of examples in many different ways. [00:01:00] We can do so programmatically. We can also add directly from real runs from our tracing project. We can also manually add examples or use AI to generate them. Each example consists of an input and an optional output. This means that you can have datasets that are comprised of only inputs.

But in this module, we're going to be curating datasets of inputs and outputs in accordance with how our RAG application takes in a question as input and returns a response as a output.

Let's go ahead and navigate over to LangSmith and see how we can create a new dataset. We'll go ahead and navigate over to the dataset and experiments pane. Here, on the left half of the screen, we can see that we can create our first dataset. Let's name it, then click Create dataset.

Creating additional datasets, looks slightly different, and we'll find more options. Navigating back to Datasets and Experiments, click the Add Dataset button. you can create a dataset by directly importing data from [00:02:00] files, like a CSV , or we can go ahead and create from scratch, which gives us an empty dataset. . Let's do that. There are a few fields that we need to input for our dataset. First, we need to give our dataset a name.

Let's call it RAG Application Golden Dataset.

By golden dataset, I mean that we're going to be creating golden ground truth examples that we're pretty confident in as a high standard for applications performance. Let's go ahead and type that in the description.

I'll also go ahead and create this with a LangSmith Academy resource tag. ~You might have noticed that I've been using this resource tag throughout our videos so far, and~ This basically helps us filter down to different resources that pertain to a particular application. The resource tags can be quite useful to filter down your resource views as you work on multiple projects. It's OK if you don't see anything here. You don't need to worry about this yet. So let's go ahead and create this dataset.[00:03:00] 

Cool. You can see that we've created a dataset here, and this is our actual dataset view. We'll talk more about these other tabs later on. The most important thing when we're looking at a dataset is our list of examples, and you can see that right now we don't actually have any examples.

Let's go ahead and grab this dataset ID and then pivot over to our Jupyter Notebook where we can create some examples for our dataset.

Now that we're in our Dataset Upload Jupyter Notebook, let's go ahead and run some code to create some examples programmatically with our LangSmith SDK. We'll show a few other ways in which you can add examples to your dataset, but I just wanted to create a few examples first so that we can take a look at the example view.

Let's go ahead and bring in our environment variables, just like we've been doing throughout this course. Then we're going to go ahead and run this code snippet here. First, we need to paste in that [00:04:00] dataset ID that we just copied.

What we can see is that we have this list of tuples where the first field is a question and the second field is a golden answer. Again, these are golden examples that I've curated and I've decided are pretty representative of good questions and answers from our application. What this code does is it goes ahead and imports the LangSmith client and then given the dataset ID that we've just pasted in, we're going to go ahead and call create examples.

This will take in three arguments. We're going to pass in the inputs and the outputs, as well as the dataset ID that we just pasted in. You can see that we're formatting this nicely to follow the format of our RAG application. Let's navigate back over to LangSmith. We can see in our dataset, we've now populated 10 examples, and these are our golden examples.

If we click into one example, we can see that we have input , and the output. [00:05:00] Cool. So now that we have this initial version of our dataset, let's go ahead and tag this version , by going to latest and clicking the tag button. we'll go ahead and call this version initial dataset.

Tags are really useful because you can version different iterations of your dataset and then test over these different iterations. Before we make any other changes, we can tag this version just so that we can always come back to and test over this initial commit if we want to. Now that we've tagged this latest version, let's show how we can add runs to a dataset directly from traces within our tracing project.

Let's go ahead and submit another trace to our LangSmith project. Navigating back to our code, we have our RAG application. I've moved the implementation over to an app.py file so that we can quickly import our app. Let's go ahead and import our application and ask another question.[00:06:00] 

Cool, so we can see that this performed pretty well. Let's go ahead and navigate back over to LangSmith and instead of our dataset view, let's navigate back over to our tracing project.

Clicking into our latest trace, we can see that at the top level, if we change this back to raw JSON output, , we have our same input and output format. Specifically, I want to call out that we can create examples in our dataset directly from runs within our trace. Here, we're going to do this with our top level trace. So we can go ahead and click add to dataset.

We can go ahead and choose our RAG Application Golden Dataset.

We're not going to add it to a split quite yet, but for now we're just going to add this as our input and output. I also want to note that we can also modify examples before adding them to a dataset. For example, I can get [00:07:00] rid of the word specific here.

Now let's go ahead and add this to our dataset. So what we just did was we added our top level run where the inputs and the outputs of the run represent the entire applications execution to our dataset. You can think of this as maybe an end-to-end integration test for our entire application.

Separately, it's also very important to be able to create unit tests for each of these individual steps within our application. As developers, it's much easier to debug or improve our application if we know exactly how each component is performing. What I would do is create a separate dataset for both of our internal sub-runs here.

I'd create a dataset specifically to evaluate our document retrieval step to see if our retrieve documents are relevant and useful. And then I'd create a separate dataset specifically to evaluate our generate response step so that we [00:08:00] know given good documents and a reasonable question, how good are we at generating a good response.

Our application here is still quite simple. You could imagine for a more complex, multi-layered application with many more sub-runs and maybe even sub-agents. It's really important to create multiple datasets and test at each of these different levels. The ability to do this from the trace view makes it really easy to build datasets from real examples that you've already tested or built on.

This is a great way to evolve your datasets naturally over time.

Now we can see that we have this new example. Just like we edited our example before we added it to our dataset, we can also edit examples within our dataset. Let's just click into an arbitrary one here. Let's say maybe I want to edit this output. I can click on the edit button and then [00:09:00] edit the actual text here.

Maybe I wanted to say it improves the performance and reliability of both LLM and agentic applications. I can submit this edit to the dataset, and now I can see that the Modified At time for this particular example has changed. Now that we have a few examples in our dataset, let's go ahead and add a schema to our dataset to ensure that our examples will follow a particular format.

We saw we had the option to do this when we were creating the dataset, but you can also do that with the edit dataset button.

Let's go ahead and define an input schema. It'll only be one field, which will be called question.

This is always going to be taken in as a string and it's always going to be required. We could also add a description if we wanted to, and we could also optionally set allowed values so this is treated [00:10:00] more like an enum. Our output schema is also just going to be one field, and this is going to be called output. It's also going to be required, and it will also be a string.

Cool. So now that we've created a schema, we've checked that all of our current examples in our dataset conforms to that schema, and we will also check that all new examples will conform to the same schema. This also makes it easier to add new examples. We already did so from a trace and we've already done so programmatically.

Now let's manually add an example by clicking add example. You can see that we have it preloaded with the schema that we've just defined. Maybe a question that we want to support is, Is there a Javascript LangSmith SDK?

And the answer [00:11:00] here is, Yes, there is a Javascript LangSmith SDK. Cool. Let's go ahead and add this example to our dataset by clicking the Submit button.

We can see our new example here. Once we've defined a schema, we also now have the ability to add AI generated examples, which is pretty cool. Let's try this out. Let's just say we want to generate three examples.

We'll actually look at our current input and output examples, and based on these questions it will add new examples. So let's go ahead and review what the AI came up with here. We can actually see that this is a good question, but the output is not exactly correct. So it supports multiple programming languages, including Python and JavaScript.

It doesn't support these other things.[00:12:00] 

The second question is answered pretty well, and this third question is also answered pretty well. So we'll go ahead and select all three of these examples, including our edited example here, and we'll save these three to our dataset.

We can see that the source for these examples is synthetic. And so now that I've added all of these new examples to our dataset, from a trace manually, and also with synthetic data generation, maybe it's time to create a new version and tag this dataset. Let's call this more examples to add . This is great over time as new examples come in. You can assess your performance against different iterations of your dataset with more questions over time, which is quite useful.

We've shown now how you can version your dataset as you make changes, but it can also be quite useful to [00:13:00] create distinct splits in your dataset. One reason to do this might be for training or fine tuning applications where you want to export your LangSmith dataset and actually train a classifier or fine tune a local LLM over the contents of the dataset.

You can create these training and testing splits directly in LangSmith. Another reason might be for CICD. Within our dataset of golden examples, there might be a subset that you think are really important to score well on whenever you iterate on your application. Let's go ahead and create a split for this, and in the future lesson we'll show you how you can test over a particular dataset split.

Let's go ahead now and create a new split. We'll select a few examples, which we think are super important to make sure that we test on properly. We'll go ahead and call this crucial examples.

We can see that in our splits view. These examples have had crucial examples added to their list of [00:14:00] splits. Cool. I can also just view this particular split when I want to.

Finally, I want to talk about a few other operations that we can take on a dataset. We can share a dataset by making it public and sharing the link here so that others can use this dataset for testing and evals.

We can also download a dataset locally as a CSV or a JSONL.

And we can also clone a dataset, ~adding all of the examples from this dataset to another one, or ~creating a new dataset with the same examples.

To recap, in this video we introduced the concept of datasets in LangSmith and we created a new dataset, adding examples to it programmatically, from a trace, manually and with AI generation.

In this next lesson we'll talk about how we can use our curated dataset examples to evaluate our application.



=============================================
File: LCA-LangSmith-C1-M2-L2-V3-Evaluators.txt
=============================================

nick: [00:00:00] In this video, we're going to introduce the concept of evaluators in LangSmith. In the last video, we talked about datasets and how they're comprised of ground truth examples for our application. When we make changes to our application, such as adding a new prompt and we evaluate over the same dataset, we want to be able to measure metrics like accuracy so that we can know empirically whether or not the change we made actually improved the application.

This is where evaluators come in. Evaluators in LangSmith operate over an example from your dataset and a run of your application over that example. It can calculate metrics like accuracy or hallucination, and you can attach multiple evaluators to a particular experiment so that you can calculate many different metrics when you run your application against the dataset.

We'll talk more about experiments in the next section. Let's take a closer look at exactly how an evaluator works. Like we mentioned in the [00:01:00] last section, a dataset is comprised of an input and optionally a reference output. In our case, we have an input, which is a question from the user, and we also have a reference output, which is a golden answer that we created.

You can add an example directly from a trace that we logged in a tracing project. You can also manually add an example, or you can generate new examples with AI or other methods. From our example, we'll run the latest version of our application over the examples input, and this will create a run output.

So notice now that we now have two outputs. We have a reference output, which is our ground truth from our example, but we also now have this run output, which is what was created by running the latest version of our application over our example input. These are the inputs that an evaluator can take. An evaluator takes in the input. It takes in the reference output from the example. And then it takes [00:02:00] in the output from the run, created by running your application over your input.

With these inputs, the evaluator can calculate a variety of metrics. Let's take a look at exactly what this looks like in code and how we can define evaluators as Python function. So once again, to recap, an evaluator takes in both a run and an example and as access to the input, the reference output, and the output from the run.

Here's a very simple evaluator defined in Python code. We have a function called correct label, and we can see that it takes in three arguments. It takes in those inputs as a dictionary, the reference outputs from the ground truth example, and then the outputs from the output of the run. This function is actually very simple.

From the run outputs, we get the output field and from our reference outputs from our ground truth golden example, we get the label field and we just compare to see if these two are equal. If these two values are the same, we [00:03:00] return one, otherwise we return zero. Notice that the return type from this function is of type dictionary, and there are two keys in this dictionary.

We have the actual key. Which is going to be the name of the feedback or score that our evaluator creates. And then we have the actual score itself, which in our case is just an integer.

Cool. So that was a very simple custom code evaluator. Now let's walk through LLM-as-Judge evaluation. These are also evaluators, only they use LLMs to score how well your application performed. Typically you make use of structured outputs as well as a system prompt to give the LLM a little bit of a role, and these in conjunction will give you back a score.

In our case, we're comparing the semantic similarity of our run output and the reference output. Let's take a closer look at how we defined this LLM-as-Judge evaluator. First, we need to import our OpenAI [00:04:00] key or grab it from our environment variables. In this code snippet, you can see that first we're defining the OpenAI client.

And then we define a class that extends base model from pydantic. This class, called similarity score, only has a single field, and the description of this field is a measure of the semantic similarity between one to ten, where one is the most unrelated and ten means identical. This class is important because this is the structure that we'll pass in as the response format for our OpenAI request.

Now, let's take a look at our evaluator itself. Just like the evaluator above, we've taken the inputs as a dictionary, the reference outputs from our golden ground truth example, and then the outputs from our run, running our application over our inputs. Here, we'll preemptively pull out the pieces of information necessary for our evaluator.

From the inputs, we'll grab the question, which is the question that the user asked. [00:05:00] From our reference outputs, we'll grab the output, which is the final golden response from our application that we've already decided is a good response. And then from our run outputs, we'll also grab the output key, and this is our run response.

We then make a request to the chat completions endpoint from OpenAI. We do a little bit of role playing. We tell the model, it's a semantic similarity evaluator comparing the two meanings of two responses where the reference is the correct answer, and we're trying to judge if our new response is correct.

We'll ask it to provide a score from one to 10 where one means completely unrelated and 10 is identical in meaning. And then we just add these three fields to the prompt. We specify our response format as our similarity score class, and this means that we can be sure that our output will have the similarity score field.

And so what we finally do is we grab our similarity score back from our completion, and then we return it as our score under the [00:06:00] key of similarity from this evaluator. Let's go ahead and try this. Here I have some sample inputs. A question, Is LangSmith natively integrated with LangChain. I have my golden reference output which says, Yes, it is natively integrated with LangChain as well as LangGraph. But then we're going to pretend that from our run, we actually got a pretty bad response back that said, No, LangSmith is not integrated with LangChain.

And so when I pass these parameters into my evaluator, we're going to make a call to OpenAI. This is going to give us back a pretty low score. You can see we got a score back of one because these answers are in fact, very significantly different.

I want to note that there's an alternative way to define evaluators that takes in the run and the example itself. This is an older method that gives you access to more fields on the run and the example such as the metadata. In practice, we see that the vast majority of evaluators only use the inputs, outputs, and reference output.

And so we [00:07:00] recommend using the above way. However, there are some places in the platform that still use the run and example primitives, so we wanted to cover it here. Here our example has inputs and our ground truth reference outputs, and our run has those same inputs, but the output field contains the run response.

And so this is essentially the same evaluator that we defined above. Only instead of grabbing the fields directly from the inputs, reference outputs and outputs, we're going a layer up and starting with the run and the example. Just like before, let's go ahead and give this a shot.

Here I have a sample run and a sample example. Just like before, we have the same input for the sample run and the sample example. Our output from our example is correct. It's our golden ground truth answer, but our output for our run is incorrect. And so ultimately these are the exact same inputs that are going to our evaluator.

The only difference is how we actually grab these values from within the input [00:08:00] parameters to our function. Running this, we can see that we also get that similarity score of one, which is really low because these two outputs are in fact very different. 

​

nick: Cool. Let's navigate over to LangSmith. So far, we've introduced conceptually what an evaluator is, what parameters an evaluator takes in, and also how to define evaluators in code.

Before we define an evaluator in the UI, let's quickly take a look again at the shape of our examples. Clicking into an example, we can see that our input has a single key question and our output also has a single key output. This is going to be important for us in a moment. Now let's take a look at how we can define evaluators in the LangSmith UI.

From our dataset view, we see the Evaluators tab. let's go ahead and click on it and we'll see all of the evaluators that we've defined in this dataset. In this case, nothing so far. Now let's go ahead and add an [00:09:00] evaluator from scratch. Here I can see two main types, LLM-as-Judge and custom code. And these correspond directly with what we just showed in our notebook.

Let's try to define an LLM-as-Judge evaluator first.

We'll actually go ahead and try to redefine that same similarity score. Here, let's name it similarity score.

We'll go ahead and pick a model provider and a model for the requests that we're going to make. Here, we'll go ahead and just use OpenAI and let's go ahead and use gpt-4o-mini.

You'll need to make sure that you have your OpenAI key passed in as well in order to use this model. You can configure the model temperature here , along with other settings. once we're satisfied with our model configuration, then we can actually create the prompt for our ~auto ~evaluator.

We can also see that we already have a default prompt template [00:10:00] for the LLM. ~We can see that in this case, we're going to be passing in a little bit of a task alongside the question, the submission and the reference. ~Let's edit this. We want to make sure, the LLM knows that it's grading for similarity between the reference and submission.

Here we can see three variables that are by default in our prompt template, input, output , and referenceOutput . These variables are entirely configurable. Let's go ahead and rename input to question, which is more correct for our use case.

Now that we have these three variables in our prompt template, we need to assign values to these variables. The values that we have the access to are the input, the output, and the reference output. The input again is from our dataset example. The reference output [00:11:00] is also from our dataset example. That's our golden ground truth output. And then the output is the output from our run.

For question, let's go ahead and map input.question. For reference, we'll go ahead and use reference_output.output. We don't actually know the shape of the outputs of our run yet, but we're going to assume that that shape is going to be pretty similar to what we have in our reference dataset.

So we'll go ahead and start with output, but then we'll here also index into that output key.

Cool. Now that we've mapped our variables, let's use structured output in the Feedback configuration section to ask for a single field back called similarity.

We can give this the description.

We can change the [00:12:00] type here to Score. We have correct min and max values. Let's give them each a description. Let's go ahead and save this LLM-as-Judge Evaluator.

Cool. Now that we have an LLM-as-Judge evaluator defined in the LangSmith UI, let's go ahead and add another evaluator.

We have many off the shelf ~auto ~evaluator LLM-as-Judge prompts that we can try. You may have noticed these earlier. Starting a new evaluator from one of these templates will pre-populate the fields that we previously set manually. These can be helpful. For example, for RAG applications, Hallucination is a great one. ~Document Relevance can also be really helpful along with Answer Helpfulness.~

Let's go ahead though and try to create another prompt from scratch. We'll make this one a custom code evaluator. This custom code evaluator looks really similar to what we just looked at in our own IDE, where we have access to [00:13:00] a run and an example.

Custom code evaluators are really great for simple regex evaluations or any objective check where you can compare fields and get some information from that. We only support basic libraries in this UI. And so if you want to do more custom things like load in your own classifier or regression model or connect to an LLM or agent of your own, you'll probably want to do that through the code just like we showed earlier.

You can also test your custom code evaluators directly in this UI. And so here, I'll go ahead and uncomment this. We'll pull the output key from both our run and our example. We'll return this as our feedback score. Let's go ahead and test this. Obviously this should fail as our input run doesn't have any real [00:14:00] values in it, but it's cool that we can test this directly.

It's also neat that we've preloaded an example from our dataset so we can test directly with the shape of our dataset. In this video, we talked about evaluators and how they calculate metrics based on a run and an example. More specifically, evaluators consume the input, the reference output, and the run output.

You can define evaluators both directly in your local code, and you can also define LLM-as-Judge and custom code evaluators directly in the LangSmith UI. In the next video, we're going to tie together what we've discussed so far in the module, datasets and evaluators, under a new concept of experiments.



=============================================
File: LCA-LangSmith-C1-M2-L3-V3-Experiments.txt
=============================================

nick: [00:00:00] In this video, I want to talk about experiments in LangSmith. In the last two videos, we talked about datasets and evaluators as distinct topics, but today we're going to show how you can use datasets and evaluators together when running an experiment. An experiment can be defined as running your application over a dataset and then evaluating the performance of your application with evaluators.

If your application is run against each example in your dataset, and for each example, your application creates a new run output your evaluators then evaluate the new run outputs for each example, comparing them against the ground truths. You can attach an evaluator to an experiment in two ways.

You can attach evaluators to your experiment in the UI, like the auto evaluator that we defined in the last lesson, or locally with your SDK. And we'll see how both of these work in this lesson.

Now let's navigate over to our LangSmith dataset. [00:01:00] As a recap from our datasets video, we created a dataset called RAG Application Golden Dataset. This dataset has a few different versions as well as a few different splits, both the base split and some crucial examples that we specified.

Each example in our dataset has an example ID.

This is something that we'll use in a moment, but I want to just call this out so you can know where to find this ID. Finally, I want to call out that we set up a similarity score ~auto ~evaluator in the last video, and we can expect this evaluator to run on our experiments that we run over this set.

Cool. Now let's navigate over to our experiments pane.

Here, we don't have any experiments yet, but let's go ahead and click on plus Experiment and then Run in SDK. This is going to take us to a Get Started with Evaluations pane, which has some starter code snippets that will help us run our first [00:02:00] experiment.

Let's go ahead and navigate over to our experiments notebook in module two. As always, let's import our environment variables.

This is the RAG application that we've been working on so far throughout this course. I want to note here that at the top, we currently have the model specified as gpt-4o. We don't need to do anything right now, but we're going to come back and configure this in a moment. Let's scroll on down over to our experiments.

Here, I have a starter code snippet that should look really similar to what you saw from the evaluations pane. Let's take a look at exactly what we have here. First and foremost, we're importing evaluate, which is how we run experiments, as well as our langsmith client. We're going to go ahead and create our client, and we're going to specify our dataset name, which is RAG Application Golden Dataset.

Then we're going [00:03:00] to define an evaluator. This is just a simple evaluator that we're going to go ahead and use, but it measures the conciseness of our run output answer relative to the golden answer in our reference output. And it's here that we also have defined a target function. A target function is really important because it maps the shape of your inputs from your example, which in our case is a single field dictionary to our actual function that we want to test.

So langsmith_rag takes in a string as input. And so what we're doing is we're taking our inputs dictionary, we're extracting that question string, and then we're passing that to langsmith_rag. Now, when we call evaluate, we're going to pass in that target function, which maps our input dictionary into our langsmith_rag function.

We're going to specify our dataset name. We're going to pass in a list of evaluators that we want to run on this experiment, and these will run in addition to the auto evaluators [00:04:00] that we've defined in the UI. Finally, we have our experiment prefix, and we'll go ahead and just set this to gpt-4o. Let's go ahead and run our experiment.

We can see that the experiment output is printed out here in the notebook itself. In the next video, we'll dive into this experiments UI in LangSmith, but here I just want to focus on running different experiments with different parameters. We can see though, that we're able to create an output for each of our 15 examples, which is pretty cool.

Now, a big use case for experiments is to measure how your application performs when we change certain things, and one of these things might be the actual model. So let's now go ahead and navigate back up to our RAG application. For our first experiment, we used gpt-4o as our model, but now let's go ahead and change this to 3.5 turbo.

I want to see whether our application [00:05:00] still works if we're using a cheaper, faster model.

Now let's run our experiment again. We can see that everything else is still the same, except our experiment prefix is now gpt-3.5-turbo.

Cool. In the next video, we'll be measuring how these two different models stacked up when running our application.

So far we've been running over our entire dataset, but maybe we only want to run our experiment over a specific subset of examples. Earlier in the datasets lesson, we created various different cuts of our data. We have different dataset versions, we have different dataset splits, and at the most granular level, we have individual examples.

Let's run our experiment again, but this time only over our initial dataset. Here [00:06:00] we can go ahead and use client.list_examples. We'll pass our dataset name just as before, but we're going to specify as of initial dataset to make sure that we use this particular version.

Cool. We can see that this experiment only runs on the first 10 examples that we added. Now, let's go ahead and run an experiment on a particular split of our dataset. Like I mentioned before, we could use this code snippet in our CICD pipeline with pytest so that we always test over this split before going into production.

This is going to be our crucial example split. Just like before, we're going to use client.list _examples and we're going to pass in our datasetname, but here we're going to pass in a splits argument. The splits argument takes a list, and so we could pass in multiple splits as well [00:07:00] if we wanted to. Let's go ahead and run this.

You'll see it run over those five examples that we added to the split.

Finally, you can also specify specific data points that you want to run over by passing in a list of example IDs. This is helpful if there are just a few problematic examples that you want to test over without running over your entire dataset. Like I mentioned before, you can get those example IDs from the examples page in your dataset by clicking into a specific example and copying the ID.

Let's just run over two examples that I have here.

Nice. This experiment was pretty quick, and you can see we just ran over these two examples.

There are other parameters that we can also specify to run an evaluation in specific ways. We can [00:08:00] specify num_repetitions, which means we actually want to run our experiment over each of our inputs X times. In this case, we're going to run over each of our inputs twice. This is really good when you want to increase the consistency of your performance and make sure you're getting similar performance over examples on repeated runs.

LLMs are inherently random, and so you could pass a test on some runs, but not on others. When this experiment finishes, we'll actually see 30 such examples here, meaning that we ran over each of our inputs twice.

We can also kick off concurrent threads of execution to make our experiments a little bit faster. Here I've specified a max concurrency of three, so this is an improvement. There is a downside here to be aware of where you want to make sure you don't hit your model rate limits, so make sure you scale this value cautiously.[00:09:00] 

Nice. That was pretty quick. Finally, you can also pass up custom metadata with your experiments. A useful piece of metadata that we can later filter on in LangSmith is passing up the model name. In our case, let's go ahead and pass up gpt-3.5-turbo with our experiment. This can be really helpful if you're running a lot of experiments with different parameters over time.

In this case, you could filter to a specific model and only look at experiments that we ran with this particular model. With the model constant, after filtering down to just gpt-3.5, you can see how changing other aspects of our application, like prompts or architecture affects our performance over time.

In the next lesson, we'll show you how to filter on your metadata in the experiments table in the UI. Finally, let's go ahead and take a look at LangSmith. We can see that we now have experiments [00:10:00] populated in our experiments pane, and our evaluator data is trickling in as well. In the next video, we'll do a deep dive into this experiment's UI and show you how you can compare the results of different experiments as well as track progress over time.

To recap, in this video, we showed you how you can run an experiment. An experiment means to run your application over a dataset and evaluate its performance by defining evaluators. Experiments can be run locally in code using the LangSmith SDK, you can run an experiment over an entire dataset or just a specific version or split, or even specific examples, and you can also run an experiment with other parameters like repetitions, concurrent threads, or passing up metadata.



=============================================
File: LCA-LangSmith-C1-M2-L4-V3-Analyzing-Results.txt
=============================================

nick: [00:00:00] In the past few videos, we've put together a dataset of golden examples, defined evaluators in our code and in the LangSmith UI and also run a few experiments. In this video, we're going to show you the difference experimentation can make. We'll show you how to use the LangSmith UI to compare these different experiments on different versions of our application or over different cuts of data, and we'll see how we can draw conclusions and make decisions to improve our application.

Let's start off in the LangSmith UI here. You can see that we've run nine experiments in total, and each of these experiments has two metrics created from the two evaluators that we defined. As a reminder, our Is concise evaluator was defined directly in our code from which we ran the experiment with the SDK.

Our similarity evaluator was defined in the UI as an LLM as judge evaluator. Note that any evaluator defined in the UI, whether as LLM is [00:01:00] judge or custom code, will automatically run over all experiments that are triggered on this dataset. Whereas if we define an evaluator in code, we need to attach that evaluator in the evaluate call to the SDK.

We can see that we have default charts created for our ~two ~metrics. This shows how the values of conciseness and similarity have changed throughout our different experiments on our application. While in the last section we were mostly focused on different parameters with which we could run experiments, these charts are a great way to assess ~over time ~whether or not the changes we make to our application actually improve it.

When we change a prompt or update an architecture and continue to run experiments on each iteration of our application, we want to see how these compare to different versions of our application. And charts are a great high level view for that progress over time.

We can also add filters over our experiments to look at a particular [00:02:00] subset of our experiments. Let's try this out. We can add filters on feedback scores , metadata, as well as other items . Let's try filtering down to all of the experiments where our model name passed up was GPT-3.5 Turbo. If you remember, we only actually did this for one of our experiments, so this filters down to that single experiment.

This is a great tool though for finding the experiments once you've run a bunch of them. It's also a great way to compare experiments where you can hold one or more variables constant. It can be helpful to only look at experiments for this particular model so that you can then assess how other changes, such as prompts, architecture, et cetera, affected the performance of your application.

Cool. Let's get rid of this filter for now.

Heading back to our experiment view. Recall that experiments two and three that we ran were with the exact same application and code over the entire dataset. The only thing that we [00:03:00] changed was we swapped the model from GPT-4o to GPT-3.5 Turbo. Let's go ahead and click into this first of the two. .

This experiment used GPT-4o. First let's take a look at some of our display options. I typically like to look at the full input and output text of shorter experiments. This gets unwieldy with larger experiments with larger inputs and outputs, but it can be really helpful to see everything. There is also a diff view, which will highlight differences between the referenceOutputs and outputs.

We can also reveal all of the feedback and metrics on the runs within our experiment. In our case, they're already all visible. 

Now, in this view, we can see each of the full examples in our dataset. We can see the input and reference output from our dataset example. We can also see the experiment output as well as the feedback scores and some metrics.

Looking through our examples, we can see how the GPT-4o [00:04:00] version of our application performed against each of them, both in regard to the conciseness and the similarity. We can also jump from each of our experiment runs into the experiment trace itself, so we can see exactly what happened in this trace.

We can see that we passed in our target function and that this called LangSmith RAG, and then we go through the full flow of our application as normal. It's going to be really helpful to take a really close look at exactly what's going on in our application when we run over one of our dataset examples. From here, we can jump directly to the example, for a closer look as well. 

Now that we've taken a closer look at the individual runs within our experiment over each example, let's take a closer look at how our evaluators were able to gather feedback. Let's look at our LLM as judge similarity score evaluator. We can see that this evaluator [00:05:00] execution is actually a run itself.

Let's go ahead and click into this evaluator.

This takes us to a new tracing project called evaluators. All evaluator runs are logged to this project, so you can always take a closer look at your evaluator runs once you've finished an experiment. Here we can see that our final prompt was our exact LLM as judge prompt with our question, our run output, and our reference output .

We can also see that we made use of structured outputs, and we got the similarity score back with tool calling from OpenAI. This feedback score was then attached to our actual experiment run. Information on the tool can be found here. This should look familiar.

Examining an evaluator run can be really helpful, to give you some deeper insight into how an evaluator got to the score that was returned. Practically, this is also really useful for debugging your [00:06:00] evaluators if they're failing on some error or if the evaluator scores are inconsistent with what you'd expect. Let's head back to our ~first ~experiment.

Finally, we can see that we can filter within an experiment as well. This includes looking at specific thresholds for feedback scores or other stats like certain metadata keys. This can be helpful to see a subset of the runs within your experiment that you're interested in. Let's take a look at all of our not concise responses.

Cool. We can see that we had four of them. Now that we've taken a close look at how we can analyze a single experiment, let's compare two experiments side by side. ~There are two ways to add an experiment to this view. You can do so through the top of the page by clicking on one experiment and then clicking on another experiment.~

You can do this by clicking the +Compare button to add [00:07:00] another experiment to our review. Now we're comparing our initial experiment and our GPT-3.5 Turbo experiment side by side. I can see how my two experiments performed on my different metrics. First, we have this feedback chart up here that shows us that GPT-4o was on average more concise than turbo was. I can also see that GPT-4o was slightly less similar across the board than GPT-3.5 Turbo was. 

We also have metrics on latency , token count, and cost . Let's take a look at the latency. This is also interesting. It tells us that GPT-3.5 Turbo was quicker on average than GPT-4o was, and this makes sense.

From here, we have to analyze whether or not any performance improvement is worth a slight increase in latency from the user's perspective. Token count and cost would be other factors to consider.

Using the Charts menu , I can add or remove these [00:08:00] summary charts. Let's go ahead and get rid ~now ~of these summary charts. Now let's actually take a closer look at our individual examples. First, let's toggle the similarity. Here we can see exactly how GPT-3.5 Turbo scored against GPT-4o for each example.

We can see in red when it was less similar and we can see in green when it scored more similar. In our case, for both of our metrics, a higher score is better. But we can also toggle this in the comparison view to show what highlights as green versus red.

You can also add more experiments to this view. For instance, if we ran another experiment with Claude 3.5 Sonnet, we could compare its performance against our two existing model experiments. We can also remove any experiment from our comparison.

This view here is really helpful for looking at the individual examples in your dataset and seeing where different versions of your applications performed [00:09:00] well and where different versions of your application have room for improvement.

To recap, experiments are a really powerful tool to see trends in your application over time as you continue to make changes and try out new approaches. LangSmith allows you to deep dive on a single experiment, looking at each run over your dataset examples, and also each evaluator run that scores your application.

You can also compare multiple experiments side by side in LangSmith, seeing exactly which versions of your application performed well on which specific examples. Experimenting over your application regularly will give you the confidence and hard data to make changes in production. Very rarely is there a single best cookie cutter approach for a use case.

Experimentation and evaluation are essential for the long-term success of any LLM application.



=============================================
File: LCA-LangSmith-C1-M2-L5-V3-Pairwise-Experiments.txt
=============================================

nick: [00:00:00] In this video, we're going to be walking through pairwise experiments in LangSmith. Sometimes it's not so easy to score how two different versions of your application performed when evaluating each of them in isolation. In a lot of cases, it's not abundantly clear whether an answer by one prompt versus another is actually better.

When you're changing architecture, models, prompts, or something else, it can be helpful to compare head to head instead of scoring individually. Pairwise evaluation is especially helpful when it's difficult to directly score an LLM output, but easier to compare two outputs. Comparing head-to-head might make it easier to tell if one answer is better than another.

This can use either a heuristic, such as which response is longer, or an LLM with a specific pairwise prompt. The output of a pairwise evaluator is a feedback score on each of our experiments, typically indicating the order of preference between our multiple experiments. [00:01:00] Let's take a look at some starter code in our Pairwise experiments notebook to see how we can compare the outputs of our two experiments.

As always, we'll start by importing our environment variables. Let's walk through a new task that we've set up for this example. This breaks away from the RAG application that we've been using throughout so far. Let's say we have a salesperson named Bob. Bob is a salesperson for an automotive company and he has a lot of deals which can be hard to keep track of.

Bob wants to use an LLM to summarize what happened in these deals based on some of the meeting transcripts. Right now, Bob is iterating on a few different prompts, trying to find one that will give him the best concise summarizations of his deals. Bob has curated a dataset of these deal transcripts.

Note that this dataset is not a golden dataset. It doesn't have a ground truth, golden reference output. Let's take a quick look at the dataset. [00:02:00] As we can see, the dataset is just a collection of deal transcript inputs. Bob wants to compare a few different prompts to see how good they are at summarizing these transcripts.

Now that we have this data set of deal transcripts, let's run some experiments.

As we run our experiments, we're going to use a typical LLM as judge evaluator to try and gauge how good our summarizations are. Like we've done in the past, we'll make use of structured outputs with our LLM as judge and ask for a score from one to five, with one being for a bad summarization, and five being for a great summarization.

We're going to provide both the transcript from our dataset and the summary from the output of our LLM prompt. Cool. Now, with this evaluator, we're going to go ahead and experiment with two specific prompts that Bob has put together. One is a good prompt. Concisely, summarize this meeting in three sentences and make sure to include all of the [00:03:00] important events.

Let's go ahead and run this first. We'll run evaluate, passing in our summarizer as the target for evaluation, our dataset, our evaluator for our summary score, and an experiment prefix of good summarizer so we know which experiment this was.

Cool. Taking a look at our outputs, we can see that all of our examples scored pretty well, according to our summarization grader. Now let's run an experiment with a worse version of our prompt. This is just going to be simpler and ask for a one sentence summary. It might still be decent, but it's not going to be as good as our concise and clear instructions above.

Awesome. Now we have two experiments. For each experiment, we ran a different prompt over our deal transcripts to try and summarize them. To a human, it might be clear that the outputs from our [00:04:00] first experiment are probably better given the clearer instructions that we provided. That being said, the scores here are also really good.

It's hard to compare these two experiments when we're viewing each experiment independently. Instead of comparing the outputs of these experiments independently, let's compare these experiment outputs, head to head against each other to figure out which is better. We can do this with a pairwise evaluator.

Pairwise evaluator functions can take in any subset of the following arguments. We can take in an inputs dictionary, which are the inputs corresponding to a single example from our dataset. We can also take in outputs, which is a list of dictionaries. In this case, it's a list of the outputs produced by each experiment over our given input example.

We also have reference outputs. This is just a dictionary, and it's the dictionary of outputs associated with that example from our data set. For most cases, you'll typically use inputs, outputs, and reference outputs. Runs and examples are useful only if you need [00:05:00] some extra trace or metadata information outside of the actual inputs and outputs of the application. So these are also accessible for you to use as well.

Cool. Let's take a look at our specific pairwise evaluator function. First, I'm going to define two prompts here. Judge System Prompt asks our LLM as judge to be impartial and to generally choose which summarization is a better summary of the input transcript.

In our human prompt, we want to provide the meeting transcript, the summarization from our first experiment and our summarization from the second experiment. As a reminder, we're directly comparing the two experiment outputs in this case. Let's take a look at how we do that exactly in our evaluator function. Here we define a function called ranked_preference.

Of the various potential parameters we just talked about. We take in inputs and outputs. So we don't actually use the reference outputs here, mostly because our dataset doesn't contain any. Similar to the LLM as judge evaluator [00:06:00] that we defined above. We're going to make use of structured outputs again. This time though, instead of asking for a score of how good the summary is, we're going to ask for a preference score of one or two.

We're going to ask that it returns one, if the first experiments output is better, and two, if the second experiments output is better. Otherwise, if our LLM as judge can't decide, we ask it to output zero if it thinks it's a tie. Like we mentioned earlier in the slides, our pairwise evaluators return a list of feedback scores for the different experiments that we're evaluating.

In this case, if our preference score is one, that means we prefer our first experiment. In this case, we're going to return one and zero to show a preference for the first experiment. Likewise, if our preference score comes back as two, this means that the LLM as judge preferred the second experiment output. And so this way we're going to return zero and one to show a preference for the second.

Finally, if it doesn't [00:07:00] return one or two, this means our LLM as judge evaluator thinks that the two experiments were tied, and so in this case, we're going to return zero and zero to show no preference. Awesome. Now that we've defined our pairwise evaluator function using an LLM as judge, let's go ahead and run this evaluator with the same evaluate function that we've been using previously.

This time though, instead of specifying a target function, we'll specify a tuple of experiments that we want to evaluate against. Note that these experiments need to be run individually ahead of time before we can compare them with a pairwise experiment. Let's go ahead and copy the names of our two experiments.

[00:08:00] Finally, we'll pass in our pairwise evaluator into the evaluators list. Let's go ahead and run this evaluation.

Awesome. Now let's click into the results. Taking a look at the Pairwise Experiment UI, we can see that we're already comparing these two experiments. We have our input, and once again, there's no reference output, and here we can see the outputs from our good summarizer and our bad summarizer.

Now we can see our original evaluator scores of five on these experiment outputs, and so there really was no difference when we compared them independently. However, when we go head to head, we can see that the ranked preference prefers the good summarizer every single time. Because this comparison was head-to-head, this means our LLM as judge thought that this response [00:09:00] was always better than this response.

This is really useful because now we can be confident in assuming that our first prompt actually performs better. To recap, we just created and ran a pairwise evaluator over two of our existing experiments. This allowed us to compare our two experiments head to head, and we used an LLM as judge to decide which of the two experiments that we preferred.

Pairwise evaluation is really helpful when it's difficult to directly score an LLM output, but much easier to compare multiple outputs.



=============================================
File: LCA-LangSmith-C1-M2-L6-V3-Summary-Evaluators.txt
=============================================

nick: [00:00:00] In this video, we're going to talk about summary evaluators in LangSmith. So far we've seen evaluators defined that operate over a run and an example, calculating metrics based off of the inputs, reference outputs, and output. The calculated metrics have all been for a specific run over a specific example from our dataset.

Some metrics can only be defined on the entire experiment level as opposed to the individual runs of the experiment. For example, you might want to compute the F1 score of a classifier across all of the runs in an experiment kicked off over a dataset. These are called summary evaluators. Instead of taking in a single run in example, these evaluators are only meaningful if they take in a list of each and calculate a single metric from the entire dataset.

For example, for F1 score precision and recall, you need to know the number of true positives, [00:01:00] false positives, true negatives, and false negatives over your dataset. These metrics don't really have any meaning for a single example, and so we can only look at them in the context of the entire experiment.

Let's navigate over to our notebook, summary evaluators, and take a look at how we set up summary evaluators for our experiments. First, let's make sure that we have all the necessary environment variables set. We're going to introduce a new task here, specifically geared towards a use case where summary evaluators are helpful.

Here we have a public dataset of statements that have been classified as toxic or not toxic. We're testing an LLM with a simple prompt and structured output on how well it's able to classify these statements as toxic or not toxic. Let's take a quick look at our dataset. Cool. Following the link from our notebook, we have navigated over to our [00:02:00] dataset called toxicity analysis.

Here our inputs are a series of statements and we have their corresponding reference outputs, which denote them as toxic or not toxic. There are some tricky examples in here where I've used negative words in a calm manner, which should be deemed as not toxic. Let's see how our LLM classifier does. Here we have a very simple prompt that just classifies a given statement as toxic or not.

Now, it's important to me that I'm able to classify each individual example correctly, but I also really care about the confusion matrix across the entire experiment. I want to know how many false positives and false negatives I have. In this case, false positives are when I incorrectly classify a not toxic example as toxic and false negatives are when I incorrectly classify a toxic example as not toxic.

This is really important to me because I'd rather have more false positives than any [00:03:00] false negatives. These fields affect the precision and recall of my application, both of which feed that F1 score. So here I have a summary evaluator that calculates the F1 score. Summary evaluator functions get access to a variety of fields.

These are the fields that summary evaluator functions get access to. You have inputs, which is a list of the dictionary inputs from the examples in our dataset. You also have the corresponding outputs, which are the output dictionaries that are produced from running our target over each input. You also have the reference outputs, which are the corresponding golden ground truth reference outputs from the examples in our dataset.

Those are the three that are most commonly used, but you can also use the run and example abstractions directly with the runs and examples lists. Here, our f1_score_summary_evaluator iterates over the entire list of outputs and reference outputs in order to calculate the [00:04:00] precision and recall and combine these into a popular metric called the F1 score.

Note that this F1 score can only be calculated across the entire experiment. It's not meaningful for a single example. We don't have to worry too much about the implementation here, but note that we're aggregating the numbers of true positives, false positives, and false negatives. Cool. Let's go ahead and run this experiment.

Note that we pass in this F1 score summary evaluator to the summary evaluators list in the evaluate function.

Now let's take a look at our experiment in LangSmith. Try navigating over to the experiments page on the dataset, If you don't see anything, try navigating to Application. Select all applications. Then choose the Toxicity Analysis dataset. We can see that we have the F1 score calculated across this entire experiment.

To recap. Some metrics like precision recall or F1 score [00:05:00] can only be calculated across an entire experiment and are not meaningful for a single example. You can calculate these metrics with summary evaluators. Summary evaluators take an entire list of runs and examples from our experiment in order to calculate metrics across the entire experiment.



=============================================
File: LCA-LangSmith-C1-M3-L1-V3-Playground.txt
=============================================

nick: [00:00:00] In this video, we're going to talk about the playground environment in LangSmith, which is used for prompt engineering. When we think about prompts, we usually think about them as hard-coded strings that tell the LLM exactly what to do. A lot of times though, there are inputs that will be passed in to create a prompt for a particular user, and so a lot of what we're going to be doing in LangSmith is going to be centered around prompt templates, which have templated variables that are hydrated by a user at runtime.

Moving from these hardcoded strings to prompt templates gives users more flexibility. LangSmith's playground is built specifically for quickly iterating on different prompts and prompt templates.

This is the playground UI in LangSmith. You can navigate to the playground from the left sidebar here. ~And playground is found under the prompt engineering section.~

You can see on the left side here we have our prompting section and a brief list of [00:01:00] messages. This is a chat prompt template. In our case right now, it's just a system prompt that gives the LLM the role of a chatbot and the human question. Notice that the question right now is templated as a variable, and we can enter that variable here under this input section on the right hand side.

When we run our prompt, we're going to generate an output, which will show up in the output section. Here we have a dropdown that allows you to select a prompt template to start from. This connects to LangChain Prompt Hub, and there are a lot of prompt templates stored here. But let's actually go ahead and build our prompt from scratch for now.

Let's ask a not so simple question. What is the meaning of life?

Here, I can click start to execute the prompt, but I can also use the command enter hotkey to immediately run.[00:02:00] 

So you can see that our LLM by default has a pretty decent answer. Note that on this left hand side, we can also add messages to mimic the full conversation between a user and an LLM. Let's go ahead and add this output as a new output message, and then try asking a follow up question.

Cool. We can see that we can ask a follow up question. Now let's go ahead and get rid of these extra messages. And now let's give our LLM little bit of a persona.[00:03:00] 

Let's go ahead and run this again.

We can see that changing the system prompt dramatically changes our output. So far we've been using OpenAI's gpt-4o-mini model, and I've been able to do this because I loaded in my OpenAI secret. In the playground, I can also quickly test out different models from different providers. If I click into this, I can change the provider and the model for this chat interaction.

This is also where you can configure different hyper parameters for the model, such as the temperature, the max output tokens, et cetera. You can also save these configurations for later use. [00:04:00] This can be particularly helpful if you're using something like Azure OpenAI, where you need to specify an endpoint.

You could save this endpoint in a configuration and so you could quickly load it for future use.

 For now, let's go ahead and use Anthropic, claude-sonnet-4-6. 

We can see that sonnet takes a longer time to respond than 4o-mini did. And we can see these metrics pop up here next to the response, including the total token usage and latency. Now maybe I want to directly compare sonnets performance against gpt-4o-mini's. I can do this by hitting the plus prompt button here.

This will [00:05:00] duplicate my prompt. So now I have prompt A and prompt B in this large prompt section at the very top. Now for one of these prompts, I can change the model provider back to OpenAI gpt-4o-mini. Let's see how these two different providers perform side by side against the same prompt.

While this is a toy example here, testing out your task with different models and different prompts is a great way to compare performance ~and also see the trade-offs with latency and token cost.~ Let's go ahead and adjust our prompt for sonnet to try and make things a little bit better.

Nice. We can see that this is closer to what we want, which is a short and sweet quick response. [00:06:00] Now, let's just say that I like the first prompt better. I can go ahead and get rid of my second prompt. So we can snap back to this more condensed UI. Another thing that you can do in this playground interface is run with a few different options.

So far, we've seen our responses come back in a streaming format, but we can also run them in a non streaming way, and we can do this by turning off streaming in the run options. Let's go ahead and disable streaming and try running this again.

Now that we've disabled streaming, we can also run this with repetitions. Repetitions are really useful to improve consistency and just double check that you're able to respond to a question correctly every time. This can be very useful if you have a high temperature or if you're dealing with a prompt that is a little bit finicky or complex and want to be sure that you can consistently perform well against this certain input.[00:07:00] 

Let's go ahead and run this with two repetitions.

And now we'll see two outputs for our prompt.

Now a few chat models allow for extra features like output schemas, or tool calling. Let's go ahead and add an output schema.

An output schema ensures that the model's response will follow a certain format. If you're using a model that doesn't support and enforce JSON schema out of the box, we'll compare the model's output against the Pydantic schema that you've defined. Let's go ahead and call this output schema extract_meaning.

The description will just be to extract the meaning of life.[00:08:00] 

Now, let's define the actual output scheme that we want. The property here is just going to be called meaning. It's going to be required, and we're going to make sure that it's a string. Here, I could set allowed values. This would mean that we would essentially get an enum back. In this case, I want the response to be freeform.

We're going to not allow additional properties in this case, we only want this particular field. And finally, we're going to turn strict mode on. This is only supported with OpenAI models, but effectively make sure that the return will match the function definition. So let's go ahead and run our prompt without repetitions.

Cool. We can see that we've identified meaning. In addition to an output schema, I can use tool calling to mimic how my prompt would respond if it had access to a certain number of tools. [00:09:00] Let's go ahead and get rid of our output schema and we'll add a new tool called find_meaning.

This tool is going to take in a single argument called thesis_on_life, and we're going to pretend that we have a Python function that given thoughts on life, can find meaning for us.

Once again, we're not going to allow additional properties and we're going to turn on strict mode.

Running this again, we can see that our LLM decides to call our tool and invokes find_meaning with this thesis_on_life. Note crucially, that the LLM does not have to call this tool. Let's go ahead and ask a different question [00:10:00] unrelated to this tool.

You can see that this response is normal. It's up to the LLMs discretion whether or not to call one of the tools that you've provided it with. For more specific information on tool calling, I'd recommend checking out how your chosen model provider handles function calling. So far, we've been showing you how you can use LangSmith's playground environment to test over a single prompt at a time.

Now we're going to show you how you can run an experiment directly in the playground interface over an entire dataset of examples. The first thing that we need to do is create a dataset for us to run our experiments over. Let's go ahead and import our environment variables in our playground experiments notebook.

All we're going to do here is run this code snippit that creates a very simple dataset. [00:11:00] This dataset is going to be called sample questions. It's just going to be three very simple questions just to illustrate how we can run over dataset in LangSmith's playground. Let's jump back over to the LangSmith interface.

Let's go ahead and reset this playground to the default. ~The first thing that we're going to do is~ Navigate over to this set up evaluation button here. We're going to go ahead and pick sample questions. Note that you can also evaluate just over a dataset split, but in our case, our dataset doesn't have any splits right now.

So let's just go ahead and click on sample questions. Here we see this tabular view pop up at the bottom. Each of our inputs and each of our reference outputs are laid out here. Let's go ahead and just run this as is with gpt-4o-mini and the default system prompt of, You are a chatbot, passing in this question from the user.[00:12:00] 

You can see that the question has been templated as an input variable, and this is going to get piped to this input field here.

We can see that the first attempt was quite robust. Let's go ahead and edit the system prompt just a little bit.

Now let's run this again.

Cool. We can see that we get a little bit closer to what we expected to see. If we go ahead and click into this experiment, this will navigate us over to the experiments page. You can see that the name of the experiment means that it's generated from the playground, and we can see our reference output and our generated output from the playground here.

[00:13:00] To recap, we just walked through the functionality of the LangSmith playground. You can think of the playground as a sandbox for you to quickly iterate on LLM prompts. We also showed how you can run experiments over datasets from the playground, which is really useful when you want to test a single step of your application.



=============================================
File: LCA-LangSmith-C1-M3-L2-V3.1-Prompt-Hub.txt
=============================================

nick: [00:00:00] In this video, we're going to talk about the Prompt Hub in LangSmith. The Prompt Hub is a solution for versioning, storing, and iterating on your prompts over time. Most LLM developers will share the experience of hard coding their prompts directly into their code. Maybe you throw your prompts into a config file, which is a little bit better, but still there's no great solution for versioning your prompts as you iterate on your application over time.

LangSmith's Prompt Hub is a great place for storing these prompt templates. As part of a prompt template, you can store a list of messages, usually a system message, and typically also at least a human message that's passed to the chatbot. These are templates, and so you don't just need to hard code strings, but you can also provide templated variables that the user will input at runtime.

This prompt template also stores a model configuration, including the information about the provider, the actual model [00:01:00] itself, and other hyper parameters like the temperature. Prompt templates can also potentially store an output schema that you want to create from the model. And so with all of this, we have a versioning scheme that allows you to commit to the same chat prompt template, and update it over time.

You can use this prompt template quickly to iterate in playground, and you can also pull this prompt template into your own code via the SDK. Let's walk you through how you can do this. To start, let's navigate over to the Prompt Hub in LangSmith. You can find the Prompt Hub ~under the prompt engineering section~ in the left hand side bar.

Let's go ahead and create a new prompt. ~By default, ~We're going to create a chat style prompt, which takes in a list of messages,~ but you can also create instruction style prompts, which provide instructions with a single message. Cool. Let's go ahead and create our chat style prompt. ~This takes us to the playground interface.

First, we'll set this to gpt-4o-mini. Let's go ahead and add a system prompt with a bit of a pirate persona, [00:02:00] and we can also add a templated variable.

We can also add an output schema here. Let's add an output schema that just tracks whatever the LLM responds with.

Cool. Now that we've iterated on this prompt a bit, let's go ahead and save it to our prompt hub. We can do that by clicking the save button here. Now let's go ahead and name our prompt. We can call this one [00:03:00] pirate-friend.

We can see that new prompts are private, by default. If it's private, it means that only users in our workspace can see it. But if it's public, it means that anyone can see it. ~For now, let's just keep it private.~ Cool. Let's navigate back over to our prompt hub. Let's walk through exactly what information we have when we save our prompt.

First, we have our actual structured prompt template here where we have the system prompt, the question, and then the structured output. We also have our chat model configuration stored. We have our provider, which is OpenAI, and we can see that we use the gpt-4o-mini model. All of our hyper parameters are stored here as well.

At any point, we could also choose to make this prompt public so that anyone can use it. Or use Permissions for more granular access. We can also fork this prompt if we want to use this as a starting point, but create a net new prompt based off of this one.[00:04:00] 

One of the coolest parts of prompt hub is that we can actually take this prompt and use it locally within our code. Let's go ahead and copy this code snippit here.

Cool. Now let's navigate over to our prompt hub notebook in module three. As always, let's make sure we load in our environment variables.

Let's go ahead and pull our prompt from the prompt hub. First we'll paste in that code snippet that we copied from the UI. We can see that this imports Client from langsmith and pulls in the name of our prompt. You must remove these two lines for now . Let's see what we got. We can see that we have a structured prompt. We can see that this includes the prompt template itself, and that this also has the schema for the structured output.

Now let's go ahead and invoke this prompt with our two inputs, question and language. [00:05:00] By printing this out, we can see that we now have a hydrated chat prompt value. We can see that the system message mentions that you should only speak Spanish and that the human message has been populated with the question.

Now let's convert these messages to OpenAI format using a converter imported from LangSmith. This translates our messages interface into the accepted format by OpenAI. Then we'll pass these messages into the chat completions endpoint from the OpenAI client, and get a response.

We can see that the response came back in Spanish and my Spanish isn't very good, but it looks like we're not a captain yet.

Let's go ahead now and pull this in again, but with an additional flag of include_model equals true. For security reasons, this means we need to specify our OpenAI key. Or, if we're pulling from a trusted prompt, [00:06:00] use secrets from env equals true to allow the key to be accessed from our local environment variables. 

~By default, as you saw above. ~With include_model equals true, we ~didn't~ pull down the model configuration with our prompt. We also get back a runnable binding, which is a LangChain object that allows us to run our prompt on the same model configuration that we saved. Note that this is not required and is just an extra bit of functionality we have if you're able to use LangChain.

Now, if we invoke our chained prompt and runnable binding, we can see that we get that AI message output back using our saved model. Now, let's say I actually want to iterate on this prompt. Let's navigate back over to the prompt hub. Go ahead and click on the playground button . This takes us back to the playground interface, and now we can iterate on our prompt.

Let's change this prompt to say that [00:07:00] we're actually a pirate from the future, specifically the year 2,500. Now let's go ahead and hit this commit button. This will create a new commit on our existing prompt. Navigating back to our prompt, I can take a look at our commits in this pane here . I can see the commit from earlier, and I can see this commit that I just made a few seconds ago.

~Clicking into this commit, ~I can see the latest version of my prompt, and now I can also pull down this latest commit with this hash code.

Navigating back to our notebook. Let's go ahead and pull down that specific commit. Again, we'll paste and remove these two lines. 

Just like before, we're going to hydrate the prompt with a question, What is the world like. And the language, which in this case we'll use English. Then we'll convert our messages to OpenAI [00:08:00] format and pass it to the chat completions endpoint.

Cool. We can see that we respond just like a pirate, and we talk about the year 2,500, meaning we did use the latest version of our prompt. Now, one other feature that I want to talk about is pushing prompts programmatically to the prompt hub through the SDK. You can pull prompts down, but you can also push prompts up.

Here I've defined a simple RAG prompt. The only slight tweak is that it mentions that users can only speak French, so this model should always respond in French. From this prompt, we'll go ahead and create a new chat prompt template, and then we'll use push prompt from the LangSmith client to push this prompt template up to LangSmith prompt hub.

Cool. It's also worth noting that you can push up a prompt as part of a runable sequence, and this will basically allow us to [00:09:00] store that model as well. Here we've done essentially the same thing. Only now we've specified a chat model with ChatOpenAI and gpt-4o-mini. We'll create a runable sequence with the prompt template and the model, and then we'll push this up to the prompt hub as well.

Cool. Let's take a look at these prompts in LangSmith.

Taking a look at french-rag prompt, we can see our chat prompt template. Taking a look at the Runable sequence, we can see that we also have our model configuration saved up here.

So to recap, we just walked through how you could save prompts in the prompt hub. These save prompts include a list of templated messages and optional model configuration, and also optionally some structured output.

You can pull these prompts directly into your code, and you can also [00:10:00] push these prompts up from your code with the SDK. In the next video, we're going to walk through a practical use case of the playground and the prompt hub using our RAG application as an example.



=============================================
File: LCA-LangSmith-C1-M3-L3-V3-Lifecycle.txt
=============================================

nick: [00:00:00] In this video, we're going to take what we've learned about Playground and Prompt Hub and tie it all together with a real example using our RAG application. Let's go ahead and start directly in our notebook. This is going to be the Prompt Engineering Lifecycle notebook. As always, we're going to import our environment variables first.

I've moved our RAG application over to an app.py file. And so we can go ahead and just import this RAG application and give it a question, How do I set up tracing in LangSmith with at Traceable?

Cool. We'll come back to this notebook in a moment, but for now, let's navigate over to LangSmith. Let's go ahead and click into our langsmith-academy tracing project. Here we can see that latest trace that we've sent. Clicking into this trace, once again, we can see our entire [00:01:00] run tree. One of the components of which is our call_openai run.

As a reminder, we log this run as a run type of LLM because it's our actual chat invocation for OpenAI. From here, let's go ahead and click into the playground.

Jumping into the playground, I can see that I've preloaded information from this particular trace. I can see that my system prompt is here and I can see that I also have a human message, which consists of the context and the question. Then I can see my current output here as well on the right hand side.

First, let's go ahead and abstract away our context and question variables.[00:02:00] 

Cool. Now if I run this again, I can iterate on this particular question with this particular context. We can see that this generation looks largely the same. One thing that I've noticed is that, while this is a correct answer, it doesn't really help the user. If the user asked how they can set up tracing with traceable, it'd be really helpful to provide a code example to that user as well.

So let's go ahead now and iterate on our prompt a little bit. We'll add a little snippet here that says, whenever possible, provide a Python code example to help the user get started.

Cool. Now let's run this again with the same context and the same question.

Okay. I can see that I [00:03:00] successfully got this code example, and so maybe this prompt is better for this particular example. To be a little bit more sure, let's try running this with a few repetitions.

Clicking through each of my repetitions here. I can see that in each, while the code is a little bit different, we did get a code example. And this is exactly what I wanted. At this point, I'm feeling pretty good about our prompt, but to be sure, let's test over a dataset.

Navigating back to our code. Here, we have a snippet that will create a dataset for us about technical questions. Note that this dataset is going to be geared specifically towards the call OpenAI run within our run tree. It's a dataset built to specifically test the prompt that we provide in our call OpenAI [00:04:00] step.

Given a question and given some formatted documents as a string, how can we get the best answer possible? This is different from the end-to-end testing dataset that we worked with earlier in this course. We're specifying a dataset name of technical questions. We're using the LangSmith client to create this dataset, and then we're preparing our inputs and outputs such that the inputs will be composed of the question and the context and the output will just be the answer to the question.

Cool. Now let's navigate back to LangSmith and test over the technical questions dataset that we just created. Now that we're back in the playground, let's select our technical questions dataset to test over. I can see that the inputs each contain a context and the question, and I can see that our output just contains our reference golden ground truth output.

We probably would [00:05:00] want some sort of similarity evaluator defined. For now, I think it'll be enough just to compare them side by side. Since we only have three examples. Let's go ahead now and run this without repetitions.

We can see that for our run tree example here, we provide a code example. We also provide a code example for our context manager, and we do so as well for the traceable decorator. Now after testing with repetitions and now also testing over this dataset with different examples, I'm pretty confident that our prompt is actually working well for this use case.

Just like we showed before, now that we're pretty happy with this prompt, let's go ahead and save it. We'll go ahead and create a new prompt called rag_with_code, and we'll keep this private for now.[00:06:00] 

Now that this prompt has been saved, let's go ahead and actually use it in our code. We'll scroll to the bottom and we'll copy this code snippet here.

Navigating back to our notebook. Let's go ahead and pull down our prompt. Specifically, we don't actually want the model provider here. We want the user in our application to be able to use whatever model they want. So for now, we'll just be working with the chat prompt template. Now let's edit the code of our application.

We'll go ahead and get rid of this rag system prompt.

Now in our generate response step. Instead of manually formatting these messages, we'll go ahead and get rid of this and we'll un uncommit these two lines of code. The first line here invokes our [00:07:00] pull down prompt with the context and the question variables, and this formats that prompt into a string.

Now we'll take that list of messages. We'll pass it into this converter utility, and this will give us back a list of messages in the OpenAI format. And we'll pass this list of messages into our call OpenAI function, which will eventually connect with the OpenAI client.

Cool. Let's give this new prompt a try.

Awesome. We can see that in our output, we do have a simple code example. Now that we have our code hooked up to the prompt hub. If I were to go back to the LangSmith interface and continue to edit and iterate on this prompt, making new commits, my code would reflect the latest commit, which is quite powerful. I no longer have to change my code every single time I update the prompt.

To recap, [00:08:00] we just walked through an end-to-end example where we used the playground and the prompt hub to help iterate on a particular prompt within our application.



=============================================
File: LCA-LangSmith-C1-M3-L4-V3-Polly.txt
=============================================

nick: [00:00:00] In this video, we're going to talk about ~the ~Polly in LangSmith. Despite the importance of prompting for the success of LLM applications, the tooling for prompt engineering remains limited. Polly is our answer to this. Polly uses an LLM agent to help you improve your prompts, which is pretty meta.

Let's navigate to LangSmith and take a quick look. We're here, in the playground interface in LangSmith. We can go ahead and access Polly by clicking on the bird icon in the lower right corner . Polly is our LangSmith assistant. It can be a useful way to experiment and develop prompts, tools, and output schema. Beyond that, Polly can also answer questions about LangSmith, explain concepts, and help with debugging, tracing, datasets, evaluations, and more. It can be accessed from almost anywhere in LangSmith. But for now, let's just see how Polly helps develop prompts in the playground. ~Notice that you can open the canvas for each of our prompts so that we can make this as custom as we want to.~

Let's go ahead and try to rewrite our pirate friend prompt using Polly . As we can see, there is a chat interface where users can ask the agent to write, update, or [00:01:00] comment on existing prompts. First, we'll set the agent's LLM to the latest from OpenAI. Let's go ahead and ask the agent to give our chatbot the persona of a pirate.

Cool. We can see that the prompt updated in the playground ~. We can always go back and look at previous versions of our prompt too.~

~If we click on, Use this version, on our new prompt, that will activate our new prompt for us to use. Stepping back into the canvas, you can also toggle on this Diff view to see the differences between the current and the previous version of the prompt. This is super helpful to see exactly what changed as a result of our prompting agent.~

There is a dedicated button in the playground UI, which will have Polly optimize your prompt. 

In addition to asking for edits directly, you can also generically ask for feedback. If you're unsure about the quality of a prompt, you can simply ask, How would you improve this prompt?

We can see that the agent will provide suggestions for some updates, and then we can [00:02:00] follow up with commands to make the updates that we want to. You can also manually edit the prompt directly in the playground . Let's go ahead and add some more specific persona.

In this case, we're going to give our pirate the persona of losing their leg while fighting a huge Kraken.

Now jumping back into Polly , I want to show how we also have the control to ask our LLM agent to edit just one specific part of our prompt. Let's go ahead and see if we can just change this example to talk about a battle. ~To do this, we'll just highlight the example and ask to change it, to be an example about a battle.~

Cool. We can see that the example is now about a really fierce battle with roaring cannons and splintering masts! 

I also want our agent to generate a templated variable within our example. In this case, this will be the pirate's name [00:03:00] . 

Now let's go ahead and ask the question. And we'll go ahead and name our pirate Polly.

Cool. We can see that our system prompt is a mixture of the prompt that Polly generated for us and our own edits, and also that we answered this question correctly.

Awesome. Now, if you have multiple users writing your prompts and iterating together on your application, it's important to add easy ways for prompts to maintain consistency. Just like how we run style and perf checks over our code before we push to GitHub, we may want to do the same thing with our prompts . Things like standardizing language complexity, prompt length, grammar, formatting, etc... You might try specifying these individually to Polly. Or, like we've [00:04:00] seen earlier, click the Optimize my prompt button to have Polly improve the prompt using best practices.

~In the prompt canvas, we do this with quick actions~  You may also want to save as you go, if you like what you have at any point. .~ By default, there are quick actions that lets you standardize language complexity, along with the length of your prompt. Users can also create custom quick actions which are accessible across the entire workspace. For instance, you might create quick actions to fix the grammar, to format examples in a certain way that you want to, or other types of standardization that are important for your organization.~

~Setting up a quick action involves naming it and setting up instructions that are passed as a prompt to our LLM agent. Once a quick action is created, it can be used by anyone in the workspace. This is really important for standardizing prompts across a product or even the entire organization. For example, clicking fix grammar here will update our examples to include better grammar and allow us to view any changes made in the diff view. In this case, all we can see here is a little bit of punctuation actually changed.~

To recap, Polly empowers users in their prompt engineering lifecycle. We can leverage LLMs to help us write better prompts according to our own specific requirements. ~And we can use quick actions for custom standardization and collaboration across our entire organization to make sure that our prompts are doing exactly what we want them to.~ 



=============================================
File: LCA-LangSmith-C1-M4-L1-V3-User-Feedback.txt
=============================================

nick: [00:00:00] In this video, we're going to talk about feedback in LangSmith. Feedback is a really big topic in LangSmith. So first we're going to introduce what feedback is and what shape it takes, and then we're going to take a closer look at user feedback in particular, which is the feedback that we get from the end users of our applications.

Feedback is really important because it allows you to understand how your users are experiencing your application and whether or not they think the application is actually performing up to standard. As we mentioned a little bit earlier in this course, feedback is a concept that lives at the run level.

LangSmith makes it really easy to collect feedback for these runs and view it in the context of the run. You can also filter on different feedback scores to look at a particular subset of your runs.

There are two main types of feedback that LangSmith supports, and that's categorical feedback and [00:01:00] continuous feedback. Categorical feedback is typically anything that's one of many categories, for example when you're classifying some trait into one of many groups. Then you have continuous feedback, which typically corresponds with some sort of numerical score. There's a range for the score, a min and a max, and the actual score falls somewhere in that range.

Let's look at a concrete example of categorical feedback. Feedback is represented as a dictionary. You have a key, which is the name of the feedback field, and in our case we're looking at is_correct. For categorical feedback, we have a value which corresponds to the string, typically, which represents that category, though it could be another type as well.

In our case, that value is yes, but it could also be no. It could also be the string succeeded or failed. On the other [00:02:00] side, for continuous feedback, we're going to have that same key, which is the name of the feedback field, and we're going to have a numerical score for the continuous feedback.

All feedback in LangSmith is associated with a feedback tag. This is that key that we were just talking about. Feedback tags are shared across a workspace, and this means that multiple users from different projects in your workspace can reuse these same tags. We'll show you how you can create and also manage these feedback tags in the LangSmith UI. Cool. Let's go ahead and take a look at LangSmith.

With some of these concepts in mind, the first thing that I want to show is where you can find the feedback for a particular run. For my project view, let's just click into the last trace and expand that run tree. We can see that there's a feedback pane here, and note that because this is a run tree, any feedback at this top level is going to be on the root run or [00:03:00] at the trace level.

You can also create feedback on the individual runs within that tree. So let's go ahead and do that now.

Here I've clicked into my generate_response run. I can see I already have a few tag recommendations here. These buttons let you quickly add recently used tags. If you're starting fresh, you may only see this Add feedback button. Let's click this button. These are all the tags that we have access to in our workspace.  Select the is_concise tag . ~One for correctness and one for conciseness. Let's go ahead and tag this as correct, and~ Let's go ahead and give this a conciseness score of maybe three. We refresh, and can see that the tag and score have popped up.

Now let's go ahead and add another tag. Similarity, this time. Let's give it a score of one. Then refresh . 

We can also create new tags and any tags that we create here will be accessible to the entire workspace as well. [00:04:00] When I want to create a new tag, I can pick the type, which will be freeform, continuous or categorical, and then specify some fields for that particular type. But for now, let's just go ahead and use what we have ~.~

~Let's go ahead and give this a value of five.~

In addition to providing feedback ~in the annotation pane~ through these tags, we can also add standalone comments or notes. Click the three dots to reveal more actions, and click on this pencil icon. ~That's going to open up our annotation pane. From this annotation pane, ~Then we'll write our note.

Cool. Let's take a closer look at this feedback ~pane again.~ Like I mentioned, all of this feedback is for our generate_response run. We can see that the source for each of these fields is User , and that means that we've generated this feedback through the UI. We can also see the different keys and the scores in this case. ~Note that because those were all continuous pieces of feedback, we don't have any values associated with them.~ And finally, when we added our note, this added a comment.

If I were to click back up [00:05:00] to our top level trace, we wouldn't be able to see any feedback because there's no feedback at this root level run.

Now let's take a closer look at where we can manage our entire list of feedback tags. We want to navigate over to the settings here and navigate to this feedback tags tab . Here I can see all of the tags in my workspace and we can also create new tags here, but like we just saw, we can also do it in line whenever we need them.

So far we've talked about how we can add feedback directly to our traces and runs through the UI, and we've also shown you where you can see all of these feedback scores in the feedback pane. Now I want to walk you through how you can also add feedback programmatically. One thing that we'll need here is a run ID, so let's go ahead and copy a run ID from our latest trace.

Specifically, let's do this for the retrieve_documents run.[00:06:00] 

Let's navigate over to our notebook here called publishing feedback, and let's go ahead and import our environment variables. 

When you're providing feedback programmatically through the SDK, you need to know the run ID. And so let's go ahead and paste this in.

We can create feedback through the LangSmith client, specifically through the create feedback function that takes in a run ID, a key and a score or value. We're also going to pass in an optional comment here on this piece of feedback. Let's go ahead and run this cell and create some continuous feedback on this run.

Now let's take a look in LangSmith.

We can see that this feedback has shown up, and crucially, we can see that the source here is API. This means that this feedback was created [00:07:00] programmatically through the SDK. Our key is sample-continuous, and our score is seven, and we also see our comment. 

Now let's head back and create some categorical feedback. This time, the key is called sample-categorical, and the value is going to be a string that says No.

Cool. Now we see that second piece of feedback. The source is also API, but this time we have a value and no score as this is a piece of categorical feedback. 

Like I mentioned above, we need to have the run ID in order to provide feedback. That flow that we just walked through of copying the run ID from the UI and then updating feedback was very manual and doesn't really scale.

So how can we actually add feedback entirely programmatically? We can pre-generate a run ID. A use case for this might be if you have a front end application. This application's in charge [00:08:00] of hitting your backend service, which actually invokes your LLM application and creates your trace. Let's say there's a button in the front end that allows your user to give some feedback right after running the application.

In order to give that feedback, you need to have that run ID. And so what we're going to do here is we're actually going to import the UUID library and we're going to generate a predefined run ID.

This here is just a sample function that's decorated with at traceable.

When we run this function, we're going to pass in an extra parameter called LangSmith Extra. This is the dictionary, and for the key run ID, we're going to pass in our predefined run ID. Now what this does is it creates a new run. Just like any other function that's been decorated with traceable. Let's take a look at this in LangSmith.[00:09:00] 

Clicking into our latest run, we can see that the run ID is the exact same as the one that we just generated. And there's no feedback on this yet, so let's go ahead and add some.

So now in our code, we have access to this UUID and we can directly create feedback with that UUID. Let's go ahead and just call it user_feedback and pass in a score of one.

Navigating back to the feedback pane, I can see that API feedback popped up right here. Note that you can create feedback directly from your front end, such as with our JavaScript SDK for LangSmith, or your front end could make another request to your backend where you already have this run ID.

This way entirely in our code, we've created the run ID itself, then run the application with our run ID and then finally provided this [00:10:00] feedback.

One more case that I want to talk about is when you can't actually expose your API Keys or other secrets to the client, or in this case, our front end application. What we can do to get around this with LangSmith, is we can take that predefined UUID and create a pre-signed feedback token from that ID with the name of the feedback that we want to create.

Let's take a look at how this works. Just like before, we're going to generate a run ID. Here, we're going to use the LangSmith client and create a pre-signed feedback token with this run ID, but then also with the name of the feedback that we want to create.

Cool. Just like before, we're going to run our sample function with LangSmith Extra and pass it in that run ID.

Now that our run has been created, we can use that pre-signed feedback URL and just send a request to give it [00:11:00] the feedback score that we want.

Cool. Let's take a look in LangSmith.

Clicking into our latest trace, we can see that we do have that user pre-signed feedback score of one.

As a recap, in this video, we introduced feedback in LangSmith and specifically how we can get feedback from users. We can create feedback manually in the UI and we can also programmatically create feedback with the LangSmith SDK. To do this, we need the run ID of the run that we want to create feedback for. So we can either pre-generate the run ID or even generate a pre-signed URL in order to create feedback entirely programmatically. In the next section, we'll talk about another way to create feedback with annotation queues.



=============================================
File: LCA-LangSmith-C1-M4-L2-V3-Annotation-Queues.txt
=============================================

nick: [00:00:00] In this video, we're going to introduce the concept of annotation queues in LangSmith. We've already talked a little bit about feedback in LangSmith and why it's really important to gather feedback on your application. We've shown you how to do this manually on traces in the UI, and also how you can create feedback programmatically.

But how do we introduce some process on how we can gather feedback from humans? The answer is with annotation queues. Annotation queues are a user-friendly way to quickly cycle through and annotate data. Users will be presented with inputs and outputs from particular runs of interest, and then they'll be asked to create feedback on those particular runs.

You can also edit an example from the annotation queue and directly add it to a dataset for use in some later offline testing. Annotation queues are also great for subject matter expert users who might not be actively developing the application, but can give good feedback on how your application is [00:01:00] performing.

Let's go ahead and navigate directly to the annotation queue section. ~under evaluation.~

We don't actually have any annotation queues yet, so let's create a new one.

We'll call this Simple RAG Application AQ.

We can also give it a description.

Here we have the opportunity to create a default dataset. This is the dataset that by default, it will be easier for our users to add examples to. Let's go ahead and select our RAG Application Golden Dataset. This is our golden ground truth dataset that we've been using for our end-to-end examples.

Now I have the opportunity to create an annotation rubric. This is basically a rubric for all of my human annotators to follow as they work through the queue. We can leave some high level instructions like, please only score [00:02:00] the fields that you're comfortable with.

Now we need to add some desired feedback to our rubric. Here we have the full list of feedback tags from our workspace, and we can also create new tags, just like before. Let's go ahead and add a continuous field, is_concise. ~Conciseness,~ And let's also add a new categorical field, is_correct.

We can also give granular instructions on both of these fields on how we want them graded specifically for our examples.[00:03:00] 

We can also specify how many reviewers we need per run to mark it as done. For us, I think we can just leave this as one, but we could also require that all workspace members have to review the run. Reservations are also an important concept. Reserving a run locks it for your review for a set amount of time.

And so this basically is a means to ensure that you don't get multiple people trying to add feedback to a single run at the same time. We'll just leave the reservation off for now. And so with this rubric, let's go ahead and create our annotation queue.

Clicking into our queue. We don't have any examples yet, so let's go ahead and add some from our tracing project.

Let's go ahead and click on one of our traces and add this to our annotation [00:04:00] queue.

In addition to adding a trace to an annotation queue from the project level, you can also add individual runs to an annotation queue from within the trace view itself. Let's go ahead and click into this trace. For us, we probably want to do this at the top level still, but you can also add individual runs to an annotation queue.

We'd probably want to set up different annotation queues for different levels of the run tree, as each run will probably have its own rubric on what makes it successful. The rubric for retrieved documents probably looks very different from the rubric for generate response. Let's go ahead and add this top level run to our annotation queue.

Cool. Those are two ways you can manually add to the annotation queue. In the next module, we'll also show you how you can set up some [00:05:00] automations to automatically send your traces to this annotation queue. But for now, let's go ahead and take a look at our queue. Here, I can see that there are two items in my queue.

I can see the nicely formatted input and output for my application, and once again, this is end to end, so all I see is the input question and the output response. If I wanted to, I could also view the raw input and the output. From this view, I can also immediately jump back to the run. This is helpful because I can look at these individual steps or see other information, like other feedback on the run or the metadata on the run.

Finally, I need to fill out my rubric. So having taken a look at this question and the provided output, I do think that we are correct in this case.

I also do think the answer was reasonably concise, so I'll give it a score of eight. [00:06:00] I can also add notes if I want to, but this is optional. Now that I'm done here, I can just click next and add my feedback.

That removes that example from my queue, and now I'm looking at the other example that I added. Let's grade this really quickly. It seems fairly concise, so I'll give it a score of nine, and it also seems to be correct. I actually think that this example is good enough to go into the golden dataset. And so for this example, I can go ahead and click add to dataset . Let's choose the RAG application Golden Dataset here.

This is a great way to build up your testing datasets over time, as you can have subject matter experts actually review traces and determine if they belong in your golden dataset. Awesome. We just added this example to our dataset. Now I'll go ahead and mark this one as done as well. Let's head [00:07:00] back over to our tracing project and let's take a look at this trace that we just reviewed.

We can see that we have our feedback now added onto it, which is pretty cool. To recap, in the previous video, we showed you how you can annotate a run directly and also how you can annotate a run programmatically. In this video, we showed you how you can annotate runs with annotation queues in a streamlined manner that makes it easy for a lot of folks within your organization to contribute to annotating your data. 



=============================================
File: LCA-LangSmith-C1-M5-L1-V3-Filtering.txt
=============================================

nick: [00:00:00] In this video, we're going to talk about filtering in LangSmith. Filtering is something that we've seen a little bit in a few different places, and it makes it easy for you to look at a subset of your runs that you care about. You can filter at various different steps and various different locations in LangSmith. And today we're going to walk through a few of these.

First, let's start in our tracing project. There are several ways to create a filter from here. You can create it from this Add filter button . You can create a filter with full text search, just looking for text matches. Or you can also create a filter from the filtering shortcuts on the sidebar here. ~ ~

~There's already one default filter that's been set, Is Root equal to true. This means that~ The default view for this table is all of the root level runs, or in other words, the runs that exist at the trace level. Let's quickly walk through the different kinds of filters that you can [00:01:00] create.

You can filter for specific inputs or outputs that match a certain field. If your inputs or outputs are in a dictionary format, you can also look at specific keys and values within that dictionary. ~We already talked about the Is Root filter.~

You can also filter for the name of a particular run. Earlier in module one, we also introduced run types and you can filter for these particular run types such as LLM Retriever or Chain. Latency is a really good metric to filter on when you're looking for longer runs, and you can also look at the status of your run, such as success or error. Or you can filter for a certain type of error that you're running into.

Earlier on in this course, we introduced metadata and how you could pass up metadata information with your runs, including the model provider with a name. That metadata and also tags are accessible to filter on here. ~And finally,~ You can filter on feedback scores, values or [00:02:00] sources, or just for particular run ID. You can also filter for a particular trace ID, thread ID, token count, or cost. 

Those were a lot of different types of filters, but let's go ahead now and just add a filter for latency. Let's say that we want to look for all root level traces that took longer than three seconds to complete. As soon as I submit this field, my table live updates, and now I can see all of the root level traces that have a latency of at least three seconds.

Let's click into one of these to confirm.

Cool. Now, so far we've only been looking at root runs. In order to filter for intermediate runs within a trace, we need to toggle, from Traces to Runs .

Now our table is updated to include all of the individual runs that took longer than three seconds, so we're no longer only looking at those top level traces. [00:03:00] Another common flow is to filter for any intermediate runs, which are part of a trace whose root run has some attribute. To extend our current example, we might want to filter for all runs that are longer than three seconds where the root trace was successfully completed.

So in order to do this, we're going to click on advanced filters and we're going to add a trace filter. These filters will apply to all of the parent runs of the individual runs that we've already filtered for. Let's go ahead and filter to where status equals success.

So now what we're looking at are all of the individual runs that took longer than three seconds that are a part of traces which were successful. On the other hand, we might want to search for runs which have specific types of sub runs. So when we were looking at trace filters, we were looking above our current run.

Now we want to [00:04:00] look within and look at our sub runs. An example of this could be searching for all traces that have a sub run with the name call_openai. This is useful when call_openai might not always get called, but you want to analyze all of the cases where it is. Let's go ahead now and get rid of these existing filters.

We'll look at top level traces. And now we're going to add a tree filter. This filter is just going to look for runs with the name of call_openai. Cool. So now our table is updated to include all of these top level traces. Let's go ahead and confirm that these traces contain call_openai, which does appear to be the case.

You can also save filters to be reused in the future. Save filters are associated with a single tracing project and are not accessible across all tracing projects. [00:05:00] Saving filters can help you organize your traces and quickly find relevant traces more easily. Let's go ahead and save this current filter.

We'll go ahead and call it contains_call_openai. We saw that after we saved this filter, it became available in this filter bar as a quick filter for us to use. And as always, we can snap back to our default view of root runs. You might also want to copy a filter that you've constructed. Maybe you want to share this with a coworker, reuse it in the future, or use this filter in the SDK.

Let's go ahead and navigate back to our contains_call_openai filter.

~In this filter view,~ I'm going to click copy ~in the upper right hand corner,~ and specifically I'm going to copy our tree filters. This is going to give us a string in our raw filtered query language. We can see what this looks like if we examine our raw query. [00:06:00] Now that you've copied a filter. Let's say you've shared it with a colleague.

Your colleague can come into the same view and paste that string in here, and this will still apply that filter on top of any existing filters that you have. Like I mentioned earlier, you can also use these raw query strings in the SDK when listing out our runs.

Navigate over to our filtering notebook in module five. As always, first we'll import our environment variables. The LangSmith SDK client has a function called list_runs, which pulls down runs from LangSmith. When doing this, you can pass in a filter in the form of a raw query string. Let's try this out. First, we're going to paste in our copied filter here.

Now we're going to call list_runs with the LangSmith client. We specified the project, which is langsmith-academy, and we've also specified our filter and the start time, meaning we just want to look at traces from the last day. [00:07:00] Let's go ahead and print this out.

Cool. You can see we got a long list of runs here. I also want to note that you can also pass in trace and tree filters in the list runs function as well. And those will also be raw query strings written in our query language.

Cool. Let's head back to LangSmith and look at one of the newest filtering features that we've added.

Sometimes figuring out the exact query to specify can be difficult, and in order to make this easier, we've added an AI query functionality. This is another feature of Polly. With this, you can type in the filter you want to construct in natural language, and it will convert it into a valid query. Let's go ahead and try this out.

Cool. You can see that it created this filter correctly. [00:08:00] You can also filter runs within a trace view. Let's go ahead and click into a trace here. This allows you to easily sift through traces with larger amounts of runs. This isn't super necessary or helpful for our short RAG application, but can be very useful for larger, longer executions.

The same filters available in the main runs table view can also be applied here, and by default only the runs that match the filters will be shown. You can also filter in the threads pane. These filters are pretty much the same, but there's one extra field that you can filter on, which is trace count, meaning the number of traces within the thread.

Finally, I want to discuss a few common types of filters that we've seen from LangSmith users to give you an idea of the types of filters that you can create. It can be really useful to create a filter for all runs that end with an [00:09:00] error. This can be a great starting point for debugging, especially when your app is in production.

Similarly, it can be really helpful to look at runs that are under a certain feedback score, either tagged by a human or added by an LLM as judge. Taking a look at these bad examples can help you motivate changes to the application.

It's also helpful to look at all LLM runs that take longer than X latency to make sure that your UI is snappy and responsive for users. This is especially important in applications where you stream back LLM outputs. You don't want these to be taking too long.

Another popular pattern that we see is filtering for particular values passed up in metadata, such as a model name. This can help limit the view to only runs that you're interested in.

To recap, these were some of the common types of filtering that we saw on LangSmith. We saw a few places in the UI where you could add filters. And there are also a few others that we [00:10:00] didn't show, but the same principles that we discussed today will apply throughout the entire platform.



=============================================
File: LCA-LangSmith-C1-M5-L2-V3-Online-Evaluation.txt
=============================================

nick: [00:00:00] In this video, we're going to talk about online evaluation and how you can set it up in LangSmith. To recap from module two, we set up offline evaluations over our application by testing against the dataset. As we iterate on different versions of our application, adding new prompts, different models, or even changing the architecture, we can consistently test against the same dataset and make use of evaluators to measure metrics on our performance.

The goal was over time to see performance improve as we made changes to our applications, and also to make sure that we weren't regressing on any important metrics. With these hard metrics, we could put changes into production with confidence. Online evaluation is a little bit different. Online evaluation involves evaluating your application in production with real usage from end users.

The way that online evaluation [00:01:00] typically works is as users use, your application traces will be published to LangSmith and you'll gather a lot of production usage data. You can create evaluators over this production data to gather metrics on how users are using your application and how your application is performing.

This is really helpful because you can still measure things like accuracy and hallucination with LLM as Judge or custom code evaluators. You can also measure softer metrics like maybe the drift and the types of questions that users are asking your application.

Let's take a closer look at exactly what fields offline and online evaluators have access to and how they're different. To review, offline evaluators have access to a ground truth example from one of your datasets. It then runs a version of your application over this example, and then works to compare the reference output and the output from your run.[00:02:00] 

Online evaluators aren't tied to any dataset or example. This means that the only fields that they have access to are your run inputs and outputs. Based on these, online evaluators will calculate metrics, and then those metrics will be published as feedback on your original trace that came in.

To reiterate, we previously created offline evaluators under the Datasets and Experiments tab. Offline evaluators score batch experiments against dataset examples. Online evaluators are created under the Tracing tab. Online evaluators run automatically against incoming traces and runs . Let's take a look at how we can set up online evaluators in LangSmith. Navigating back over to our tracing project, we can see our full view of traces here. Click the Evaluators tab .~ Now, let's navigate over to this add rule button. This is where you can add rules~~.~~ Rules run on traces as they're traced live to your project. We'll talk more about rules in the next lesson, but one type of rule is an online evaluation.~

Once we click Add Evaluator, this takes us to the same UI that we saw in module two [00:03:00] when we were defining offline evaluators. And just like before we can create LLM as Judge. There are some options here like trying a template evaluator prompt or using an existing prompt.

These can help you get started faster, but let's go ahead and write our prompt from scratch this time. 

You can set up filters so an evaluator only executes on a filtered subset of your runs, and you can also define a sampling rate.

For now, we'll leave our filter to just root runs, meaning runs at the trace level, and we'll leave our sampling rate at one hundred percent , meaning we execute this rule on all root level traces.

Just like before, we need to make sure that we have our secret in LangSmith for the model provider that we want to use. We'll use OpenAI's gpt-4o-mini. Now let's set up our LLM as Judge Online Evaluator. First, I want to click into [00:04:00] one of our variable mappings and call out specifically what we have access to when defining online evaluators. Like we just discussed, when defining offline evaluators, we had access to an input from a dataset and the reference output from our dataset.

In this case, because we have an online evaluator, it's not tied to any particular dataset, and so we only have access to the inputs and the outputs from our runs. Specifically the input and output fields that we have access to are sampled from the last five traces in our project. Okay. Let's take a look at the default prompt that we've started with.

We can see that the default is just using structured output to measure conciseness and get a score back from the LLM. Let's actually go ahead and change this to something more specific to our use case. We're going to change the human prompt to, You are assessing a user's question and determining whether or not it's related to LangSmith.[00:05:00] 

I'll also go ahead and get rid of the output here because we only need information about the input . Now for a structured output schema, I want to create a field called about_langsmith.

This is going to be a Boolean. , ~ but~ we're going to go ahead and keep on strict mode here. [00:06:00] Note that we started with a sample prompt to score conciseness , which required the input and the output from our run, but now we're asking a question that's only concerned with the actual input. It's important to note that online evaluators have the flexibility to do both.

Let's go ahead and map this input ~query ~to our input question.

We're going to call this evaluator about_langchain. Once again, note that our filter is going to apply this to every trace run, and our sampling rate is one hundred percent , meaning we'll run this online evaluator on every single incoming trace. We also have the ability to apply this to past runs, getting the score on previous runs, but we're not going to do that for now.

Let's go ahead and save this.

Cool. Now we can see our first online evaluator. Let's go ahead and pivot over to our notebook for this lesson. Our notebook is [00:07:00] super simple this time. We just invoke our application so that we can trigger our new evaluator to run once. We'll load in our environment variables and then just submit a single trace.

Awesome. Navigating back to LangSmith, I can see that this trace has come in. It's important to note that online evaluators don't always run immediately, so we'll wait a few minutes to get our result. While we wait, let's take a closer look at custom code online evaluators. Let's go ahead and add another evaluator and this time we'll click code evaluator.

We can see here that there's an immediate difference from this UI than the one when we were defining offline evaluators. For offline evaluators, we got access to the run and an example, but here we only get access to the run, and specifically the inputs and the outputs of the run. We also have access to a sample [00:08:00] run from our tracing project.

The sample run is really helpful when defining our evaluator so we can see exactly what the shape of our inputs and our outputs are. An example of something that we could do in a code evaluator is maybe a re regex search to see if the term LangSmith actually shows up in the question or something like that.

We also have the ability to test our code in here on this sample run. Cool. Now that we've seen what a custom code evaluator looks like. Let's navigate back over to our trace ~.~

~Let's take a look at the logs. ~Once we're in the trace, let's look at the feedback pane. If you don't see anything yet , feel free to pause the video for a minute or two and something should show up. But after about a minute, you can see that we have ~one log here. We can see that we scored this trace with a score of one for~ our about_langsmith tag ~.~

~Let's jump into this trace.~

Here we can see a piece of feedback and we can see that it was created by an ~auto ~evaluator. The key is about LangSmith and our score is one, meaning this question was in fact about LangSmith. [00:09:00] In the last module, we talked a lot about how users can add feedback to LangSmith runs.

We've also just shown now how you can use an online evaluator with LLM as Judge to add feedback to runs as they come in. This is a really powerful tool to help you get real time feedback on how your application is performing in production.

Now that we've taken a look at how to set up online evaluations in the UI, I want to talk through a few common types of usage that we've seen for online evaluators.

Hopefully these examples will inspire you to set up a few online evaluators of your own. For document retrieval tasks, it's really important to be checking constantly for any hallucinations in the output relative to the documents that are provided. To do this, you can use an LLM as Judge Online Evaluator, and you can ask the LLM whether an answer provided by your application is grounded in the provided source documents.[00:10:00] 

The structured output that you can use in this case is to get a score back called did_hallucinate, which is a required Boolean. This is really important to make sure that the documents that you're providing your application with are being used when answering users' questions. The score might drop over time if some of the documents that you've provided are falling out of date and potentially conflicting with an LLMs pre-training.

And so if this happens, it's a good idea to double check your document quality, or maybe even try switching out the LLM powering your application. Another example of an LLM as Judge Online Evaluator is to actually just try and perceive the helpfulness of an answer to the user. This can be a simple numerical score from one to ten, and is really helpful for just getting a quick pulse on how an LLM perceives how well your application works.

This isn't the most rigorous check by any means, but it can be great in assessing how well equipped your application is to handling inputs from [00:11:00] real users. And also as your user base changes over time, this is a good quick check to see whether or not your application can also adapt.

In general, good use cases for code online evaluators involve some programmatic check that you can execute over the input and output of your run. Let's take the example of a coding assistant agent. One check we can create is to see if the code output of the coding assistant actually compiles and can execute.

You can also get more granular and see if particular libraries are imported. Custom code evaluators are quite flexible in this sense. In our example, our feedback score could be code_is_valid, a Boolean score based on if we can run our code with Python repl. Along the same lines, there are also cases where you might care to check that the output of your LLM follows a certain format.

Let's use the example of an email writing assistant. [00:12:00] Let's say that we want to make sure that we sign emails a certain way. A good way to do this check is just with a regx match. So let's say we always want to make sure that we sign an email with best wishes, comma, Nick. You could do this simple check with a code online evaluator that runs over every trace that comes in, and for every trace you could return a Boolean feedback score.

To recap. In this video, we talked about how to set up online evaluation in LangSmith. Online evaluation is a great tool to keep a pulse on how your application is actually performing in production, and a great way to get feedback without having to manually annotate a run. Finally, we just walked through a few common examples and types of online evaluators that you can create.



=============================================
File: LCA-LangSmith-C1-M5-L3-V3-Automations.txt
=============================================

nick: [00:00:00] In this video, we're going to talk about automations in LangSmith. In the last video, we talked a little bit about ~rules in the context of~ online evaluations. You may sometimes hear online evaluators and automations categorized together as automation rules, although they are setup from different locations within the LangSmith UI. Here I want to take a closer look at ~these~ automations and all of the different actions that we can take.

While you could manually process production logs from an application, it often becomes really difficult as your application scales to more users. Automations allow you to trigger certain actions on your trace data. At a high level, automations are defined by a filter, a sampling rate, and then an action. The different actions that you can take with an automation queue include adding to a dataset, adding to an annotation queue, ~performing some sort of online evaluation, whether LLM as judge or custom code,~ triggering arbitrary webhooks, like to PagerDuty, or extending the data retention.

An example [00:01:00] of an automation would be to say when the model used is gpt-4o for a root trace, and that trace took longer than five seconds, then 80% of the time we might want to add this example to a dataset.

Cool. Let's take a look at automations in LangSmith. Navigating over to our tracing project, we'll see there are two ways to add an automation, just like the two ways to add an online evaluator. One way is from the Automations tab. Another is from the Runs tab. ~And clicking into our rules pane, we can see the about_langchain online evaluator that we set up previously.~ If I click add new, then click new automation, the Create Automation Rule pane will appear. We can see that we have filters that we can define to specify which sorts of runs the rule should be applied to. We also have a sampling rate, which determines how often after the filters pass do we actually want to apply this rule.

The sampling rate is really helpful [00:02:00] because a lot of rules, in particular LLM as judge evaluators that we saw last time, can become quite expensive if you run them on every single trace. This is something that you should tweak and adjust in accordance with your application's usage volume. When creating a rule, you can also apply the rule to past runs as well.

To do this, you need to select, Apply to past runs, and you need to pick a backfill date. This date specifies when you should start applying the rule. Once you specify a date, it'll actually start from that date and apply the rule until it catches up with the latest runs from the present. This is useful when you've just gotten around to adding an automation and you wish that you had that automation already in place for the last period of time.

Cool. Let's click through the different actions that we can take here. First, we can add to an annotation queue, so we can automatically, if our filter passes, add a run to an annotation queue. [00:03:00] You can also add to a dataset. A practical use case for this might be if the user provides some good feedback on a trace, you might want to add it to a dataset of golden examples.

~We've already walked through LLM as judge and custom code evaluators.~ You can also trigger webhooks. This is really extensible and allows you to kick off actions outside of LangSmith based on the traces that are coming in from production. An example of this might be if you filter for rate limit errors specifically.

Then you can trigger a webhook to create a Jira ticket that will ask one of the engineers on your team to reach out to your model provider or double check the token. Finally, you can also extend data retention for this particular run. It's worth noting that all of these other rules when triggered will also automatically extend data retention on the matching runs. But for this rule, that's all you do and no additional action is taken.

~We also have a PagerDuty integration, which is pretty neat, and we can trigger alerts. If your organization uses PagerDuty ~Let's create an new automation rule. We'll extend the data retention for any [00:04:00] trace, when the trace's latency is at least 8 seconds. We'll name this latency check, and click save. This takes us to the Automations tab, where we'll see a list of automation rules we've created.

For a given rule, we can click into the logs and see the history of this rule being applied. It may take a minute for a log to appear for a new rule. Logs allow you to gain confidence that your rules are working as expected. If something went wrong with your rule or you think it's not being applied properly, logs would be the best place to check as they show both successful and unsuccessful errored executions of your rule.

One more important topic to discuss is that rules can be chained. What this means is that you can have one rule [00:05:00] apply to create some sort of feedback on a run. Then you can actually use another rule that will apply on that same run with the new feedback to take another action. Let's walk through an example of setting this up.

What we'll do here is we'll actually create a new run filter where we're filtering for a specific feedback score. Let's go ahead and use about_langsmith, and let's check that the score is equal to one. So we're looking for questions that were about LangSmith. Cool. So with this filter, if it applies then let's just say 50% of the time, ~or with a sampling rate of 0.5,~ we want to push that trace to our simple RAG application annotation queue that we created in an earlier module.

This way some person can go and give feedback on that run. Let's go ahead and call this rule annotate_about_langchain. Cool. [00:06:00] So now we have two rules working in tandem. We have ~one rule that's~ an LLM as judge evaluator that will create this piece of feedback, and then based on that feedback score, we have an automation that will potentially push that same run into an annotation queue.

There's nothing that you need to do to explicitly chain these rules. Rules will automatically process any runs that come into your project. In addition, any runs that have feedback added to them are added again to a queue for these rules to process. And so in this case, when the LLM as judge evaluator executes and adds feedback, our run gets added back to the queue from which rules process.

Then we'll be able to catch and see if this trace is actually about LangChain, and then 50% of the time we'll go ahead and add it to our annotation queue. Note that each rule can only process each run once, so we're protected against rules [00:07:00] repeatedly or infinitely processing the same incoming runs.

Now that we've taken a look at how to set up automations in the UI, I want to talk through a few popular automations that we've seen our users put into production.

One popular example of an automation is sampling all of the traces within your project with pretty low frequency and adding them to an annotation queue. Specifically, you'd filter for all root traces. You'd set up a sampling rate that's pretty low, maybe just one or 2% of the time, depending on your production volume.

And then the action would be to add to an annotation queue just geared for this purpose. This is a really great tool for keeping a pulse check on how your application is performing over time. Users in your annotation queue can go through and add feedback, and then over time you can see how your application's performance might be changing.

Another popular automation is to add all traces or [00:08:00] runs with negative feedback 100% of the time to an annotation queue. This is also really important. Whenever we get negative feedback from a user or maybe even from an LLM as judge online evaluator, we want to take a closer look at why that feedback was negative and potentially change our application to safeguard against these cases in the future.

They could potentially then add those examples to red team datasets from the annotation queue. We can then use those datasets to make our application more robust against these cases.

On the other hand, a great way to build up your golden datasets is to set up an automation that takes traces with positive user feedback and adds these directly to a golden dataset. By filtering for positive feedback, then taking 100% of those traces and adding them to a dataset, you have a golden dataset that grows as your application is in production.

And so over time, you can continue to test against [00:09:00] this dataset and make sure that your application is performing well in the same way that made users respond positively in the past. This is great for regression testing, especially as later on, maybe you want to make your application more complex or add more features. You want to make sure that you don't regress on things that had already made users happy.

Another important automation is to handle errors for important or sensitive applications. So if the status of the run is an error, depending on how critical the flow is, you may always want to alert PagerDuty. This is a great way for you to feel confident that your application is working in production and is not silently failing without you noticing.

Finally, I want to talk through a chaining example. Specifically, we could look at one particular piece of logic within an application, maybe a retrieved document step. [00:10:00] We could sample this 100% of the time, and then we could run an online evaluator where we could check to see whether or not the retrieved documents are relevant.

This will create a piece of feedback called irrelevant_docs. We can then set up a separate automation that looks for this particular feedback key, irrelevant_docs. If the feedback score is suboptimal, we can do a number of things such as alert PagerDuty. If we don't want to be as extreme, we can add to an annotation queue or a dataset.

To recap, we just talk through the different types of rules that you can create. Rules are really helpful as a means to quickly build up annotation queues or datasets without having to add each run manually. They're also great for online evaluations, and if you need to connect to external systems through a webhook. Rules can be chained and there's nothing that you need to do specifically to set up chaining. When you add feedback to a run, it gets requeued and reprocessed [00:11:00] by applicable rules.



=============================================
File: LCA-LangSmith-C1-M5-L4-V3-Monitoring.txt
=============================================

nick: [00:00:00] In this video, I want to talk about the monitoring tab in LangSmith. ~For this video in particular,~ We're going to first get a quick view with simple examples , which will show you how to use the UI. Then, I want to show you the monitoring tab for one of our own production applications so that we can see statistics, metrics, and insights from a real live production app.

~What we're looking at here is one of our own applications called Chat LangChain. You can think of Chat LangChain as very similar to a ChatGPT like interface. Only it has a RAG flow in the background that makes use of documentation about LangChain LangGraph and LangSmith, all of our products.~

~Clicking into one of my old threads, we can see that once a user asks the question, we do some planning and research and fetch relevant documents before providing a final answer. If you're curious, you can find Chat LangChain at chat.langchain.com. So let's pivot over to LangSmith. Here I'm looking at the tracing project for chat-langchain.~

Now I want to move over to this monitoring tab that we haven't really looked at before. The monitoring tab gives us default charts that provide insights into our projects' and applications' performance. I want to talk about the different types of statistics and metrics that we can get from this tab. Let's start by analyzing our langsmith-polly project. There are a few different sections that we're going to walk through.

The first section that we're going to talk about is traces, but before we do that, let's go ahead and set our time range to the last 30 days.

There are a few different trace metrics that we get out of the box. One ~that is super important~ is trace count, which [00:01:00] reflects the number of queries made to Polly. We can see that over the past 30 days, this count has been sporadic, with varying days and peeks of usage. We can also see this split by status successes and errors.

We can see the percent of traces that errored over time, and occasional latency spikes. Maybe we're wondering, what's behind these spikes? We can drill down into the trace to examine any point on our charts. Just click, the trace icon will appear, and then click the icon. There are a few traces within this timeframe. If we click the one with the highest latency, we can see significant time was spent by the tools, looking deep into the documents for this query. That's not the case with other traces.

~ We can also see the LLM call count. ~This next section shows LLM calls , including LLM call count [00:02:00] and LLM latency. ~This is a useful metric in particular regarding our deals with different model providers.~

~We want to make sure that we're staying within our rate limits and not approaching ranges where we'd have to worry about running into those pesky 429 rate limit errors. We also have success rates for both traces and LLM calls. Like we saw above, these dipped a little bit on November 17th, and then also recently, but our LLM calls have been going through well, which is good to know.~

~Let's remember this, and we'll come back to this in a little bit and try to look into exactly why our error rates might have spiked. The next section of charts have to do with latency. Latency is really important to monitor for your application, especially as you make changes to your app. We actually made a change earlier this week.~

~Now we have some more LLM specific metrics.~ This section is dedicated to cost and tokens . It shows costs, output tokens, and input tokens, as both total amounts, and amounts per trace. For the amounts per trace, these are shown for the average latency, P50, as well as the worst latency, p99.

~So we must have been passing in some larger context windows as a result of this change.~

The next section shows charts for the tools used in our traces: the run count per tool, each tool's median latency, and error rate ~.~

~This really ballooned $35 recently, and so after having taken a look at the charts in our monitoring view,~

Then, we have similar charts for run types.

~We can see that the cost per trace has more than five x'd. And so we can see that latency has really jumped up for our application, which is something that we're going to have to keep an eye on and decide if our performance improvements are worth that trade off. This latency had to do with a particular LLM call, so we can see that LLM latency is also increased.~

Now, this last section is, I think, one of the most important sections within the monitoring tab . This is our feedback section. Let's just switch to our langsmith-academy project for a minute. So all of the feedback that we've talked about providing over the last few modules, including feedback from users created through the SDK, feedback directly added in the LangSmith UI, feedback added in annotation queues, and also feedback from [00:03:00] online evaluators, can be seen here in these charts showing us trends over time.

~Let's talk about these two different feedback metrics at the top here. We have about_langchain and about_langgraph. This is really just a measure of what percentage of questions are about LangChain and about LangGraph. These two pieces of feedback actually came from online LLM as a judge evaluators~~.~

~We can see that over the past 30 days, LangGraph has been a bit all over the place, but LangChain has been steadily much more prevalent than LangGraph has been. This feedback view is really useful for seeing aggregated and averaged out feedback metrics over time. These trends are very important in terms of determining how we should potentially change our application.~

~And for us, maybe this means we add in more support and more documents about LangChain given the interest. Or maybe this tells us that we need to more widely promote LangGraph to get more people asking about it.~

~Finally, we have some streaming metrics. Almost all of our traces and LLM calls use streaming. An important metric here is time to first token. This is really impacted by how your application is set up and how long it takes to get that first token back from your application. If you pass in a really large context window, it can definitely also take longer.~

~Cool, so we've just walked through all of the different charts within our monitoring view. Now let's actually try and do a little bit of AB testing analysis. ~Let's switch back to our langsmith-polly project. If you remember, Polly allows the user to specify the model that they want to get an answer from. This model is passed up as metadata in our runs, which is something that we showed how to do when setting up tracing in module one.

~So now in our monitoring view,~ Let's go ahead and look at that metadata. This group by button lets us split our data based on tags, or metadata. By selecting metadata, and then model ID, we can see the performance between these different models. You can imagine also how for AB testing different prompts or even different versions of your application, you can pass up the version numbers in the metadata and then use this same view in the monitoring tab to compare performance in production.

If any data you're monitoring seems particularly alarming, or noteworthy, you can alert your team [00:04:00] automatically. Let's setup rules for a new alert. Click the Alerts tab, then click the plus alert button. For our langsmith-polly project, judging by events over the last 14 days, I think I want to setup at latency alert.

This will be for latency greater than 20 seconds. No. 30 seconds. Then we can send an alert via webhook, PagerDuty, or Dynatrace . In fact, if we want, we can have several of these actions. In reality, this might not be a worthwhile alert, but we've at least seen how alerts can be managed in the LangSmith UI . Now that you've seen how to use the Monitoring tab, let's use it to analyze a larger, real-world production application.

The next part of this video was recorded with an older version of LangSmith. The UI may look a little different, but the thought processes and [00:05:00] insights should still be very helpful for your own work!~ Because of our model split, we can see that this error rate earlier this week due to Haiku is really dramatic. Let's go ahead and click into this to discover why our Haiku requests were failing here at a 31% error rate.~

~If I click into this, it'll zoom me into this time range and navigate me back to our familiar tracing project view. Now I can see that we've pre-applied some filters. We filtered to where the model name is Haiku and status is success. But I actually want to change this to error because I want to see why these are failing.~

~So let's take a look at exactly what happened here. Clicking into this trace, it looks like we were running into a bad request error. Knowing this, we can disregard this as something truly problematic or fundamentally wrong with Haiku's execution. We were able to really quickly diagnose this issue by starting in the monitoring tab and then clicking into the traces where we saw a problem.~

~To recap, we just talked about the monitoring view in LangSmith, specifically regarding one of our own production applications, Chat LangChain. This monitoring view can give you a lot of good insights into how your application is performing. You can also analyze AB tests with this monitoring view based on the different metadata and tags that you pass up with your application.~

~And finally, you can use this monitoring view as a place to kickstart explorations into why things might be going wrong in your application.~

What we're looking at here is one of our own applications called Chat LangChain. You can think of Chat LangChain as very similar to a ChatGPT like interface. Only it has a RAG flow in the background that makes use of documentation about LangChain LangGraph and LangSmith, all of our products.

Clicking into one of my old threads, we can see that once a user asks the question, we do some planning and research and fetch relevant documents before providing a final answer. If you're curious, you can find Chat LangChain at chat.langchain.com. So let's pivot over to LangSmith. Here I'm looking at the  monitoring tab for the chat-langchain project.

~There are a few different volume metrics that we get out of the box. ~Trace count is super important , as this is just a strict measure of how many users are using our application. We can see that over the past 30 days, this count has dipped on weekends and also understandably dipped a little bit over the [00:06:00] Thanksgiving period.

We can also see this split by status, which is pretty useful. So we can see that there was a small bump in errors on November 17th, and then also a few days ago. But before that, we were in pretty good shape with just a few errors each day. We can also see the LLM call count. This is a useful metric in particular regarding our deals with different model providers.

We want to make sure that we're staying within our rate limits and not approaching ranges where we'd have to worry about running into those pesky 429 rate limit errors. We also have success rates for both traces and LLM calls. Like we saw above, these dipped a little bit on November 17th, and then also recently, but our LLM calls have been going through well, which is good to know.

Let's remember this, and we'll come back to this in a little bit and try to look into exactly why our error rates might have spiked. ~The next section of charts have to do with latency.~ Latency is really important to monitor for your application, especially as you make changes to your [00:07:00] app. We actually made a change earlier this week.

And so we can see that latency has really jumped up for our application, which is something that we're going to have to keep an eye on and decide if our performance improvements are worth that trade off. This latency had to do with a particular LLM call, so we can see that LLM latency is also increased.

~Now, this next section is, I think, one of the most important sections within the monitoring view. This is our feedback section. So all of the feedback that we've talked about providing over the last few modules, including feedback from users created through the SDK, feedback directly added in the LangSmith UI, feedback added in annotation queues, and also feedback from online evaluators, can be seen here in these charts showing us trends over time.~

Let's talk about these two different feedback metrics ~at the top here.~ We have about_langchain and about_langgraph. This is really just a measure of what percentage of questions are about LangChain and about LangGraph. These two pieces of feedback actually came from online LLM as a judge evaluators.

We can see that over the past 30 days, LangGraph has been a bit all over the place, but LangChain has been steadily much more prevalent than LangGraph has been. This feedback view is really useful for seeing aggregated and averaged out feedback metrics over time. These trends are very important in terms of determining how we [00:08:00] should potentially change our application.

And for us, maybe this means we add in more support and more documents about LangChain given the interest. Or maybe this tells us that we need to more widely promote LangGraph to get more people asking about it.

~Now we have some more LLM specific metrics. What insights can we gather about our LLMs' token consumption? ~Given that change a few days ago, we can see our token usage has really spiked here. We can see that that's also true for the number of tokens per LLM call, so we must have been passing in some larger context windows as a result of this change.

~The next section about~ Cost is also very important. This is really helpful for us to see how much money we're spending per day right now on our application. We can see that with our change. This really ballooned $35 recently, and so after having taken a look at the charts in our monitoring tab, I'm leaning towards walking back our change because of how dramatically it's impacted the cost and the latency.

We can see that the cost per trace has more than five x'd.

~Finally, we have some streaming metrics. Almost all of our traces and LLM calls use streaming. An important metric here is time to first token. This is really impacted by how your application is set up and how long it takes to get that first token back from your application. If you pass in a really large context window, it can definitely also take longer.~

[00:09:00] Cool. ~So we've just walked through all of the different charts within our monitoring view.~ Now let's actually try and do a little bit of AB testing analysis. So in Chat LangChain, just to revisit this UI, we also allow the user to specify the model that they want to get an answer from. And just like our Polly example, this model is passed up as metadata in our runs, ~which is something that we showed how to do when setting up tracing in module one.~

So now in our monitoring tab , let's go ahead and look at that metadata. ~By clicking on this metadata button here, and then searching for model name, then clicking on this,~ we get now a split view across our graphs for these different model names. We can see the performance between these different models. ~You can imagine also how for AB testing different prompts or even different versions of your application, you can pass up the version numbers in the metadata and then use this same view in the monitoring tab to compare performance in production.~

So taking a look at trace count, we can see by far gpt-4o-mini is the most popular, and this is probably because it's the default and most people don't bother to change it. We can also see that success rates are pretty good across the board, but we definitely struggle a little bit with Gemini, and Haiku very recently had a big blip.

The latency for the models is also really useful information. We can see that Sonnet typically takes the longest to respond, [00:10:00] while the rest are pretty on par. So there are a few potential takeaways here. For one, maybe we could pull Sonnet from the available models because it tends to take longer, and maybe we also remove Gemini because it's leading to some of those trace failures.

Remember that all of the graphs from this monitoring view are interactive and can be the start of a debugging or investigative flow. Let's take advantage of that. Because of our model split, we can see that this error rate earlier this week due to Haiku is really dramatic. Let's go ahead and click into this to discover why our Haiku requests were failing here at a 31% error rate.

If I click into this, it'll zoom me into this time range and navigate me back to our familiar tracing project view. Now I can see that we've pre-applied some filters. We filtered to where the model name is Haiku and status is success. But I actually want to change this to error because I want to see why these are [00:11:00] failing.

So let's take a look at exactly what happened here. Clicking into this trace, it looks like we were running into a bad request error. Knowing this, we can disregard this as something truly problematic or fundamentally wrong with Haiku's execution. We were able to really quickly diagnose this issue by starting in the monitoring tab and then clicking into the traces where we saw a problem.

To recap, we just talked about the monitoring tab in LangSmith, including its usefulness in analyzing one of our own production applications, Chat LangChain. The monitoring tab can give you a lot of good insights into how your application is performing. You can also analyze AB tests with this monitoring tab based on the different metadata and tags that you pass up with your application.

Alerts, based on the data you're monitoring, can be configured and managed here.

And finally, you can use this monitoring tab as a place to kickstart explorations into [00:12:00] why things might be going wrong in your application. 



=============================================
File: LCA-LangSmith-C1-M5-L5-V3-Dashboards.txt
=============================================

nick: [00:00:00] In this video, we're going to talk about custom dashboards in LangSmith. With custom dashboards, you can create tailored collections of charts for tracking metrics that matter most to your application. Custom dashboards are particularly useful when you only care about a few particular metrics and don't need to see all of the default information from the pre-built dashboards we saw earlier .

They're also super useful if you want to track metrics across multiple tracing projects. Let's take a look at custom dashboards in LangSmith. Navigating over to the monitoring tab in the left sidebar, we can see the different dashboards that have been created so far in my workspace. There are pre-built dashboards that come from projects, and there are custom dashboards that we'll examine in this video. Let's create a new custom dashboard by clicking on the plus dashboard button here.

We'll give our dashboard a name and a description. Let's go ahead and call it Intro to LangSmith.[00:01:00] 

Cool. Now we have an empty dashboard. Let's go ahead and create our first chart. Dashboards are comprised of multiple charts for your viewers. One cool thing about charts in dashboards is that they can calculate metrics across multiple tracing projects. If I wanted to, I could select multiple projects and aggregate statistics like the total number of runs or the total number of tokens used.

This will give me a great bird's eye view of the usage rates across all of my projects. For now though, let's go ahead and just select our langsmith-polly project just so we can have some more usage data than what's in LangSmith Academy. If you're following along, feel free to select the LangSmith Academy project or your own project.

Next, we'll select a metric. These are [00:02:00] different statistics and pieces of telemetry that we can generate charts for. For our metric, we'll start by selecting P 50 latency, or in other words, our average latency. Our preview here is showing our average latency over the last seven days for our root runs. We can change this time range too.

Let's take a look at the last 14 days. Just like in other places in LangSmith, we can add filters to our charts. By default, our charts look at all of the root runs or the trace level runs within a project, just like we do in the tracing project view. We can also filter down to a specific subset of runs.

Let's add a filter to look at where status equals error for a root run. Nothing in the last 14 days. How about the last 30? 

Cool. Now we're looking specifically at the P 50 latency when our run failed. This is pretty neat. Let's [00:03:00] set our window back to 14 days. And~ Now~ let's get rid of that filter we just added. We can also create multiple lines of data in a chart, and one way to do this is by adding multiple metrics, because we're looking at P 50 latency for our root runs right now.

I think it'd be interesting to compare this to the P 99 latency, or in other words, some of the worst latency that we see for our application.

Wow. We can see that the P 99 latency is more than double and sometimes triple what our average latency is. This is something that we'll have to keep an eye on and we can see that there was definitely a ~huge~ spike or incident on May 9th .

In addition to comparing two metrics like we're doing, so right now, we can also create different splits of data by grouping, or by creating data series with their own sets of filters. First, let's get rid of that second metric that we were comparing against.

Now these options are selectable . Taking a quick look at the runs in our graph, we can see that there are many sub runs within our Chat LangChain [00:04:00] application.

~Specifically, we have two main steps, one of which is called create_research_plan, and also conduct_research.~ A really common use case for dashboards and for charts is to compare the latency of different steps in our application. Let's go ahead and do that now.

~First, ~ Group by, can automatically split the data into multiple series. We can see the latency of steps if we group by run name. ~Let's add one data series for create research plan.~

~Our filter here is just going to filter for the name of our run, and we're going to look specifically for create_research_plan.~

~Next, we'll add another data series for conduct research.~

~Cool.~ Now, importantly, we need to get rid of that root run filter here, so we can look at our sub runs within our graph. ~This is really interesting.~ We can see that there are a few groups graphed. Let's increase the maximum number of groups, so we can see more. ~. I wonder if there's a code change that we can track this to.~

Now, let's say we want to compare the latency between different LLMs. We'll group by metadata, then model ID. For more manual and granular control, there is the custom data splits option. That means an alternate way to create this chart, is to filter for each individual model ID, and add each as a data series, one at a time. [00:05:00] 

That's one. We'd just repeat this for the remaining LLMs. We also have the option to ask Polly to create our chart. Let's ask to show daily tokens used. 

Cool.

Finally, we can display our chart as a line chart or as a bar chart. ~In our case, I think it makes more sense to look at it as a line chart. ~ Polly has already named this chart, and given it a description. And once we save it, we can now see it on our dashboard.

To recap, you can use dashboards to create customized views for specific information that you're interested [00:06:00] in. Custom dashboards can transcend tracing projects, so you can aggregate metrics across multiple projects. Custom dashboards are also a great way to create high level views for stakeholders in your product to get a quick sense of how things are going.

And finally, you can use custom dashboards to granularly analyze specific subsets of runs, including for particular steps in your application by filtering to specific names of runs, just like we saw.



