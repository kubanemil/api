# Check if an argument is provided
if [ $# -eq 0 ]; then
    echo "Error: No argument provided. Please specify the endpoint name."
    exit 1
fi

# Get the endpoint name from the first argument
endpoint_name=$1

# Build the Docker image with the dynamic Dockerfile name
if ! docker build -t endpoints:$endpoint_name -f Dockerfile.$endpoint_name .; then
    echo "Error: Docker build failed for endpoint $endpoint_name"
    exit 1
fi

if ! docker tag endpoints:$endpoint_name 010046428417.dkr.ecr.ap-south-1.amazonaws.com/endpoints:$endpoint_name; then
    echo "Error: Docker tag failed for endpoint $endpoint_name"
    exit 1
fi

if ! docker push 010046428417.dkr.ecr.ap-south-1.amazonaws.com/endpoints:$endpoint_name; then
    echo "Error: Docker push failed for endpoint $endpoint_name"
    exit 1
fi