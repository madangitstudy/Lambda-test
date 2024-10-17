{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "lambda:InvokeFunction",
      "Resource": "arn:aws:lambda:REGION:ACCOUNT_ID:function:push-notification-klaviyo-test",
      "Condition": {
        "ArnLike": {
          "AWS:SourceArn": "arn:aws:lambda:REGION:ACCOUNT_ID:function:Pax-flight-voucher-generation"
        }
      }
    }
  ]
}
