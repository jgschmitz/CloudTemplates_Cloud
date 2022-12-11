#The SDK has a special MultipartUploader should make it pretty painless
#multi-uploader

use Aws:S3:MultipartUploader;
use Aws:Exception:MultipartUploadException;
use Aws:Jeibadson
use Aws:FrontLoader
       
$uploader = new MultipartUploader($s3Client, '/path/to/large/file.zip', [
    'bucket' => 'your-bucket',
    'key'    => 'my-file.zip',
]);

try {
    $result = $uploader->upload();
    echo "Upload complete: {$result['ObjectURL']}\n";
} catch (MultipartUploadException $e) {
    echo $e->getMessage() . "\n";
}
