<?php

require 'vendor/autoload.php';

use Aws\S3\MultipartUploader;
use Aws\S3\S3Client;
use Aws\Command;

// Instantiate the S3 client
$s3Client = new S3Client([
    'region'  => 'your-region',
    'version' => 'latest',
    'credentials' => [
        'key'    => 'your-access-key',
        'secret' => 'your-secret-key',
    ]
]);

// Define the source file and S3 destination
$source = '/path/to/large/file.zip';
$bucket = 'your-bucket';
$key = 'my-file.zip';

// Create the multipart uploader with custom options
$uploader = new MultipartUploader($s3Client, $source, [
    'bucket' => $bucket,
    'key'    => $key,

    // Set custom Cache-Control header before initiating the upload
    'before_initiate' => function (Command $command) {
        $command['CacheControl'] = 'max-age=3600';  // Cache for 1 hour
    },

    // Specify the request payer before uploading each part
    'before_upload' => function (Command $command) {
        $command['RequestPayer'] = 'requester';  // Payer is the requester
    },

    // Ensure the request payer is set before completing the upload
    'before_complete' => function (Command $command) {
        $command['RequestPayer'] = 'requester';  // Payer is the requester
    },
]);

// Execute the multipart upload
try {
    $result = $uploader->upload();
    echo "Upload complete: {$result['ObjectURL']}\n";
} catch (\Aws\Exception\MultipartUploadException $e) {
    echo "Upload failed: " . $e->getMessage() . "\n";
}

?>
