# SK INTERVIEW CHALLENGE
version 1.1


0. Ensure that you can connect to the kubernetes control plane API using the provided kubeconfig file
**** Your kubeconfig has access to ONLY the namespace interview-48d539efac ****
**** ENSURE ALL YOUR WORK TARGETS THE ABOVE NAMESPACE ****


1. Deploy the sample app (docker image: gbolo/sample-app:1.2) your namespace. See below for details
  - sample app requires talking to a mysql database
  - sample app can be configured with environment variables:
      # define what port to listen on
      APP_SERVER_BIND_PORT=60061
      # define connection string for database
      # format: <username>:<password>@tcp(<host>:<port>)/<database>
      APP_DATABASE_DSN="sample:password@tcp(127.0.0.1:3306)/sample"


2. Expose the sample app with an ingress that has the hostname: interview-48d539efac.interview.vme.dev
	- The above FQDN will get registered once the object is created. Please allow a few minutes for DNS propagation
	- access the ingress with TLS: https://interview-48d539efac.interview.vme.dev
		** certmanager is installed and will take care of getting a TLS certficate **

3. Create a script that will interact with the sample app
	- sample app is a REST API. see https://interview-48d539efac.interview.vme.dev/swagger for details
	- There is a list of clients in csv format, Ensure all clients are onboarded

4. Submit all deployment code (for all steps above) for review.
	- You may zip it and email it
	- You may provide it in a git repo
