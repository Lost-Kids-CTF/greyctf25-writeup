# Sgrpc

## Challenge (804 points, 71 solves)

> Can't get hacked if they can't reach it.
>
> http://challs.nusgreyhats.org:33202
>
> Author: QuanYang

## Summary

We are given a gRPC service implemented in Go, with the endpoint `GetFlag` being public but need to be called with a request that satisfies some conditions (but the source code for the conditions is redacted).

## Analysis

From the gRPC [documentation](https://grpc.io/docs/guides/reflection/):

> Reflection is a protocol that gRPC servers can use to declare the protobuf-defined APIs they export over a standardized RPC service, including all types referenced by the request and response messages. Clients can then use this information to encode requests and decode responses in human-readable manner.
>
> Reflection is used heavily by debugging tools such as grpcurl and Postman. One coming from the REST world might compare the gRPC reflection API to serving an OpenAPI document on the HTTP server presenting the REST API being described.

gRPC reflection allows clients to retrieve the full API schema—including service definitions and message types—from a running server. This makes it possible to reverse engineer the structure of the `.proto` files without source access.

We began by extracting the descriptors using `grpcurl` (note that we cannot run `describe flag.FlagReply` or `describe flag.GetFlag` directly due to `isDisallowedMessage` implemented in `customreflect.go`):

```bash
grpcurl -plaintext -protoset-out descriptors.pb challs.nusgreyhats.org:33202 describe flag.HelloReply
```

This revealed the following message definition:

```proto
message HelloReply {
  required string message = 1;
}
```

Next, we used `protoc` to decode the raw descriptor to learn more about the services and message types (**potentially those that are not allowed to be described directly under the `isDisallowedMessage` check**):

```bash
$ protoc --decode_raw < descriptors.pb
1 {
  1: "google/protobuf/empty.proto"
  2: "google.protobuf"
  4 {
    1 {
      8: 0x7974706d
    }
  }
  8 {
    1: "com.google.protobuf"
    8: "EmptyProto"
    10: 1
    11: "google.golang.org/protobuf/types/known/emptypb"
    31: 1
    36: "GPB"
    37: "Google.Protobuf.WellKnownTypes"
  }
  12: "proto3"
}
1 {
  1: "flag.proto"
  2: "flag"
  3: "google/protobuf/empty.proto"
  4 {
    1: "FlagRequest"
    2 {
      1: "first_condition"
      3: 2
      4: 2
      5: 9
      7: "TraLaLeRo TraLaLa"
      10: "firstCondition"
    }
    2 {
      1: "second_condition"
      3: 3
      4: 2
      5: 12
      7: "cafebabe"
      10: "secondCondition"
    }
    2 {
      1: "last_condition"
      3: 1
      4: 2
      5: 6
      7: "3141592654"
      10: "lastCondition"
    }
  }
  4 {
    1: "FlagReply"
    2 {
      1: "flag"
      3: 1
      4: 2
      5: 9
      10: "flag"
    }
  }
  4 {
    1: "HelloReply"
    2 {
      1: "message"
      3: 1
      4: 2
      5: 9
      10: "message"
    }
  }
  6 {
    1: "Flag"
    2 {
      1: "GetFlag"
      2: ".flag.FlagRequest"
      3: ".flag.FlagReply"
      4: ""
    }
    2 {
      1: "Hello"
      2: ".google.protobuf.Empty"
      3: ".flag.HelloReply"
      4: ""
    }
  }
  8 {
    11: "ctf.nusgreyhats.org/sgrpc/flag"
  }
}
```

From this output, we reconstructed the important parts of the service definition:

- The relevant RPC:

  ```proto
  rpc GetFlag(FlagRequest) returns (FlagReply);
  ```

- The expected input message:

  ```proto
  message FlagRequest {
    fixed64 last_condition = 1; // 3141592654
    string first_condition = 2; // "TraLaLeRo TraLaLa"
    bytes second_condition = 3; // "cafebabe" (ASCII)
  }
  ```

To pass these conditions, we must encode the input correctly:

- `last_condition`: a 64-bit integer, must be `"3141592654"` (as string in JSON)
- `first_condition`: the literal string `"TraLaLeRo TraLaLa"`
- `second_condition`: the bytes of the ASCII string `"cafebabe"`, encoded as base64 → `"Y2FmZWJhYmU="`

---

## Approach

We first validated our `.proto` definitions by calling the `Hello` RPC:

```bash
grpcurl -plaintext -proto flag.proto challs.nusgreyhats.org:33202 flag.Flag/Hello
```

After confirming service accessibility, we sent the crafted request to `GetFlag`:

```bash
grpcurl -plaintext \
  -proto flag.proto \
  -d '{
        "last_condition": "3141592654",
        "first_condition": "TraLaLeRo TraLaLa",
        "second_condition": "Y2FmZWJhYmU="
      }' \
  challs.nusgreyhats.org:33202 \
  flag.Flag/GetFlag
```

This successfully returned the flag.

## Flag

`grey{r3fl3ct_th3_sch3m4}`

## Appendix: `flag.proto`

```proto
syntax = "proto3";

package flag;

import "google/protobuf/empty.proto";

message FlagRequest {
  fixed64 last_condition = 1;
  string first_condition = 2;
  bytes second_condition = 3;
}

message FlagReply {
  string flag = 1;
}

message HelloReply {
  string message = 1;
}

service Flag {
  rpc Hello(google.protobuf.Empty) returns (HelloReply);
  rpc GetFlag(FlagRequest) returns (FlagReply);
}
```
